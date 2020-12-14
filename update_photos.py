"""
Downloads data and files for use in the website

Obstacles
- There is a usage limit that returns a 403 error so this script can be run a few times every so often. This should be
fine since we don't update the photos often.
https://developers.google.com/drive/api/v3/handle-errors

Improvements to make on this script
- Add query for downloading just some of the files, not all
- Multithread downloading files?
- Add option for test files in CLI

Update the photos.json file
python update_photos.py --download_metadata

Download files to the photos directory
python update_photos.py --download_files

Update the metadata for files (currently, just the description)
python update_photos.py --upload_metadata
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
import pprint
import html2markdown
from mdutils.mdutils import MdUtils

TEMPORARYMOMENTS_FOLDER_ID = "1m1SBar05i6ov59CPfz_CsrGA-iwiSzxb"
SEATTLE_FOLDER_ID = "1ASIRGe59CgDIpztCJGUEtQOkGKNpVKSw"
TEST_FOLDER_ID = "1vjDZYfEf0pfTu-_qk5zWf6p3kPTvjMpS"

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

FILE_FIELDS = "id,name,description,fileExtension,imageMediaMetadata"

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
                body=new_metadata
            ).execute()
            return updated_file
        return None
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None

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

def get_service(credentials_file):
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
    return service

def main():
    parser = argparse.ArgumentParser(description="Update photos")
    parser.add_argument('--credentials_file', dest='credentials_file', default="./credentials.json",
                        help="path to the credentials file")
    parser.add_argument('--download_files', '-d', action='store_true', dest='download_files', default=False)
    parser.add_argument('--download_metadata', action='store_true', dest='download_metadata', default=False)
    parser.add_argument('--upload_metadata', action='store_true', dest='upload_metadata', default=False)
    parser.add_argument('--to_markdown', action='store_true', dest='to_markdown', default=False)
    args = parser.parse_args()

    # Validate arguments
    if args.download_metadata and args.upload_metadata:
        raise ValueError("Cannot download and upload metadata in the same run")

    # Get service and files
    service = get_service(args.credentials_file)

    param = {
        "q": "'{}' in parents and trashed = false".format(SEATTLE_FOLDER_ID),
        "fields": "nextPageToken,files({0})".format(FILE_FIELDS),
        "orderBy": "name"
    }

    # Call the Drive v3 API
    items = retrieve_files(service, param)

    if not items:
        print('No files found.')
    else:
        if args.download_metadata:
            # Saves photo data as json to be read by Jekyll
            with open('_data/photos.json', 'w', encoding='utf-8') as f:
                json.dump(items, f, ensure_ascii=False, indent=4)

            # Saves photo data as js variable to be read by js
            with open('src/photos.js', 'w', encoding='utf-8') as f:
                f.write("var photos = {0}; export {{ photos }};".format(json.dumps(items, ensure_ascii=False, indent=2)))

        if args.upload_metadata:
            item_id_to_item = {i['id']: i for i in items}

            local_items = []
            with open('_data/photos.json', 'r', encoding='utf=8') as f:
                local_items = json.load(f)

            for local_item in local_items:
                new_metadata = {
                    "description": local_item.get("description")
                }
                file_id = local_item["id"]
                update_file(service, item_id_to_item[file_id], new_metadata, True)

        if args.download_files:
            for index, item in enumerate(items[:1]):
                url = item['webContentLink']
                r = requests.get(url)

                r.raise_for_status()

                if r.status_code == 200:
                    dest = "images/photos_fullsize/{id}.{fileExtension}".format(**item)
                    with open(dest, 'wb') as f:
                        f.write(r.content)
                        print("{0}/{1} Downloaded {2} to {3}".format(index + 1, len(items), item['name'], dest))

        if args.to_markdown:
            local_items = []
            with open('_data/photos.json', 'r', encoding='utf=8') as f:
                local_items = json.load(f)

            content = ""
            mdFile = MdUtils(file_name='Seattle Draft',title='Temporary Moments')
            for item in local_items:
                photo = "![{0}]({1})".format(item['id'], "images/photos_thumbnail/{id}.{fileExtension}".format(**item))
                description = html2markdown.convert(item.get("description", ""))

                content += "{0}\n\n{1}\n\n".format(photo, description)

            mdFile.write(content)
            mdFile.create_md_file()

if __name__ == '__main__':
    main()
