import argparse
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import requests
from apiclient import errors
import os
import pprint
import html2markdown
import markdown
from mdutils.mdutils import MdUtils
import re
import warnings

# If modifying scopes, delete the file token.pickle.
READONLY = 'https://www.googleapis.com/auth/drive.metadata.readonly'

FILE_FIELDS = "id,name,description,fileExtension,imageMediaMetadata"

TEMPORARYMOMENTS_FOLDER_ID = "1m1SBar05i6ov59CPfz_CsrGA-iwiSzxb"

def get_service(credentials_file="credentials.json", scopes=None):
    """
    Creates a token.pickle file which stores the user's access and refresh token.
    This file is automatically created when the authorization flow completes for
    the first time.

    Args:
        credentials_file (str): path to google drive api credentials file
        scopes (list[str]): list of scopes of access to service

    Returns:
        googleapiclient.discovery.Resource: service to the google api client
    """
    if scopes is None:
        scopes = [READONLY]
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
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    return service

def retrieve_files(service, param):
    """Retrieve a list of File resources.

    Args:
      service: Drive API service instance.
      param (dict): parameters to pass in to getting files
    Returns:
      list[dict]: List of File resources.
    """
    files = []
    page_token = None
    while True:
        try:
            param['pageToken'] = page_token
            result = service.files().list(**param).execute()

            files.extend(result.get('files', []))
            page_token = result.get('nextPageToken')
            if not page_token:
                break
        except errors.HttpError as error:
            print('An error occurred: %s', error)
            break
    return files

def update_file(service, file, new_metadata, new_revision):
    """Update an existing file's metadata and content.

    Args:
      service: Drive API service instance.
      file (dict): file to update including id.
      new_metadata (dict): New metadata for the file.
      new_revision (bool): Whether or not to create a new revision for this file.
    Returns:
      dict: Updated file metadata if successful, None otherwise.
    """
    try:
        update = False

        for key in new_metadata:
            if key not in file or file[key] != new_metadata[key]:
                update = True
                break

        if update:
            # Send the request to the API.
            updated_file = service.files().update(
                fileId=file['id'],
                body=new_metadata,
                newRevision=new_revision
            ).execute()
            return updated_file
        return None
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None

def get_folders(service, parent_id):
    """ Get all of the folders underneath the parent folder

    Args:
        service: Drive API service instance.
        parent_id (str): id of a parent folder

    Returns:
        dict: map of folder name to folder id
    """
    param = {
        "q": "mimeType = 'application/vnd.google-apps.folder' and '{0}' in parents".format(parent_id),
        "fields": "nextPageToken,files({0})".format(FILE_FIELDS),
        "orderBy": "name"
    }

    files = retrieve_files(service, param)
    folder_names = [f["name"] for f in files]

    if len(folder_names) != len(set(folder_names)):
        # TODO: Maybe raise an error instead of a warning?
        warnings.warn("FOLDER NAMES ARE NOT UNIQUE - "
                      "Please go to the Google Drive to make all the folder names unique.", UserWarning)

    folders = {f["name"]: f["id"] for f in files}

    return folders

def main():
    service = get_service("credentials.json", [READONLY])
    print(get_folders(service, TEMPORARYMOMENTS_FOLDER_ID))

if __name__ == '__main__':
    main()
