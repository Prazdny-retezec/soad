import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from googleapiclient.http import MediaFileUpload

from google_drive import GDRIVE_CREDENTIALS_DIR

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]

TOKEN_PATH = os.path.join(GDRIVE_CREDENTIALS_DIR, "token.json")
CREDENTIALS_PATH = os.path.join(GDRIVE_CREDENTIALS_DIR, "credentials.json")

#creates oauth token, returns gdrive_service used for communicating with gdrive
def gdrive_auth():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(filename=TOKEN_PATH, scopes=SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file=CREDENTIALS_PATH, scopes=SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    try:
        gdrive_service = build("drive", "v3", credentials=creds)
        return gdrive_service
    except HttpError as error:
        # TODO Handle errors from drive API.
        print(f"An error occurred: {error}")
    
    
#upload file, return ID of the file uploaded
def upload_zip_file(gdrive_service, path_to_local_zip_file, gdrive_file_name, gdrive_folder_id = None, mime_type="application/zip"):
    file_metadata = {
        "name": gdrive_file_name,
        "mimeType": mime_type,
        "parents": [gdrive_folder_id],
    }
    # TODO add check for unsuccessful file upload
    media = MediaFileUpload(path_to_local_zip_file, resumable=True)
    # upload file to gdrive
    file = (
        gdrive_service.files()
        .create(body=file_metadata, media_body=media, fields="id, webViewLink")
        .execute()
    )
    print(f'File with ID: "{file.get("id")}" has been uploaded.')
    gdrive_url = file.get('webViewLink')
    print(gdrive_url)
    permission = {
        'type':'anyone',
        'role': 'reader',
    }
    # create link to file that anyone can view
    gdrive_service.permissions().create(fileId=file.get("id"), body=permission).execute() 
    return gdrive_url
    

            
