"""
Downloads data and files for use in the website

Improvements to make on this script
- Add query for downloading just some of the files, not all
- Multithread downloading files?

Update the photos.json file
python update_photos.py --credentials_file "C:\\Users\\Ellen\\Credentials\\temporarymoments_client_secret.json"

Download Files
python update_photos.py --credentials_file "C:\\Users\\Ellen\\Credentials\\temporarymoments_client_secret.json" -d
"""
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

TEMPORARYMOMENTS_FOLDER_ID = "1m1SBar05i6ov59CPfz_CsrGA-iwiSzxb"
SEATTLE_FOLDER_ID = "1ASIRGe59CgDIpztCJGUEtQOkGKNpVKSw"

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def retrieve_files(service, param):
    """Retrieve a list of File resources.

    Args:
      service: Drive API service instance.
      param (dict): parameters to pass in to getting files
    Returns:
      List of File resources.
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

def main():
    parser = argparse.ArgumentParser(description="Update photos")
    parser.add_argument('--credentials_file', dest='credentials_file', required=True,
                        help="path to the credentials file")
    parser.add_argument('--download_files', '-d', action='store_true', dest='download_files', default=False)
    args = parser.parse_args()
    credentials_file = args.credentials_file
    download_files = args.download_files

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
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    param = {
        "q": "'{}' in parents and trashed = false".format(SEATTLE_FOLDER_ID),
        "fields": "nextPageToken,files",
        "orderBy": "name"
    }

    # Call the Drive v3 API
    items = retrieve_files(service, param)

    # Using the file we already have
    # items = None
    # with open('_data/photos.json', 'r', encoding='utf-8') as f:
    #     items = json.load(f)

    if not items:
        print('No files found.')
    else:
        with open('_data/photos.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)

        if download_files:
            for index, item in enumerate(items[:1]):
                url = item['webContentLink']
                r = requests.get(url)

                r.raise_for_status()

                if r.status_code == 200:
                    dest = "photos/{id}.{fileExtension}".format(**item)
                    with open(dest, 'wb') as f:
                        f.write(r.content)
                        print("{0}/{1} Downloaded {2} to {3}".format(index + 1, len(items), item['name'], dest))

if __name__ == '__main__':
    main()
