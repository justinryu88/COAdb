from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build, build_from_document
from flask import Flask, render_template, request
import os
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def search_files():
    # Load the service account credentials from the JSON file
    # Fetch your credentials from the environment variable
    creds_json = os.getenv('GOOGLE_CREDS_JSON')
    
    # Parse the JSON string into a Python dictionary
    creds_dict = json.loads(creds_json)
    
    # Create your credentials object
    creds = Credentials.from_service_account_info(creds_dict)

    with open('drive_api.json', 'r') as f:
        discovery_data = f.read()

    service = build_from_document(discovery_data, credentials=creds)

    # Call the Drive v3 API to list the files in the folder
    folder_id = '1BTTgMBVhg8mG0dQ5H8e5KT-ltQUohS7B'
    query = f"'{folder_id}' in parents"

    search_term = request.args.get('search_term')
    if search_term:
        query += f" and name contains '{search_term}'"

    results = service.files().list(
        q=query,
        pageSize=3, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    return render_template('results.html', results=items, search_term=search_term)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
