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

    # Map folder names to folder IDs and their respective page sizes
    folders = {
        'COA': ('1BTTgMBVhg8mG0dQ5H8e5KT-ltQUohS7B', 3),  # replace with your folder id and page size
        'SDS': ('1jK9zt2wXqWLnpyQqrk1at0cbMJdXElpi', 5),  # replace with your folder id and page size
        'Formula': ('1Ee9JZQnIx5JO-qFGIxwGY7q5uBKXzIzJ', 50),  # replace with your folder id and page size
    }

    # Get the selected folder from the form data, default to 'COA' if none is selected
    selected_folder = request.args.get('folder', 'COA')

    # Call the Drive v3 API to list the files in the folder
    folder_id, page_size = folders[selected_folder]
    query = f"'{folder_id}' in parents"

    search_term = request.args.get('search_term')
    if search_term:
        query += f" and name contains '{search_term}'"

    results = service.files().list(
        q=query,
        pageSize=page_size, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    return render_template('results.html', results=items, search_term=search_term, selected_folder=selected_folder)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
