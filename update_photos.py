"""
Improvements to make on updating photos

Example Run
python update_photos.py --credentials_file "C:\\Users\\Ellen\\Credentials\\temporarymoments_client_secret.json"
"""
import argparse
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

TEMPORARYMOMENTS_FOLDER_ID = "1m1SBar05i6ov59CPfz_CsrGA-iwiSzxb"
SEATTLE_FOLDER_ID = "1ASIRGe59CgDIpztCJGUEtQOkGKNpVKSw"

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def main():
    parser = argparse.ArgumentParser(description="Update photos")
    parser.add_argument('--credentials_file', dest='credentials_file', required=True,
                        help="path to the credentials file")
    args = parser.parse_args()
    credentials_file = args.credentials_file

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

    kwargs = {
        "q": "'{}' in parents".format(SEATTLE_FOLDER_ID),
        "fields": "nextPageToken,files",
        "orderBy": "name"
    }

    # Call the Drive v3 API
    results = service.files().list(**kwargs).execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        with open('_data/photos.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
