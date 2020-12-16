from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
from apiclient import errors

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


def uploadFile(service, path):
    file_metadata = {'name': 'Data.json'}
    media = MediaFileUpload(path, mimetype='application/json')
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    print('File ID: %s' % file.get('id'))


def updateFile(service, file_id, new_title, new_description, new_mime_type,
               new_filename, new_revision):
    """Update an existing file's metadata and content.

    Args:
      service: Drive API service instance.
      file_id: ID of the file to update.
      new_title: New title for the file.
      new_description: New description for the file.
      new_mime_type: New MIME type for the file.
      new_filename: Filename of the new content to upload.
      new_revision: Whether or not to create a new revision for this file.
    Returns:
      Updated file metadata if successful, None otherwise.
    """
    try:
        # First retrieve the file from the API.
        file = service.files().get(fileId=file_id).execute()

        # File's new metadata.
        file['title'] = new_title
        file['description'] = new_description
        file['mimeType'] = new_mime_type

        # File's new content.
        media_body = MediaFileUpload(
            new_filename, mimetype=new_mime_type, resumable=True)

        # Send the request to the API.
        updated_file = service.files().update(
            fileId=file_id,
            # body=file,
            # newRevision=new_revision,
            media_body=media_body
        ).execute()
        return updated_file
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    updateFile(service, "1OyAttZeV8M7gqxTs7FbxfQxvls3wCuYa", "Data.json",
               "", "application/json", "C:/dev/ProgramFiles/ExpTrc/Data.json", False)


main()
