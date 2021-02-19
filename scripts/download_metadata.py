import argparse
import json
import pprint
import temporary_moments_utils

def main():
    parser = argparse.ArgumentParser(description="Download metadata from")
    parser.add_argument('--folder', '-f', dest='folder', default=False)
    args = parser.parse_args()

    service = temporary_moments_utils.get_service()
    folders = temporary_moments_utils.get_folders(service)

    pprint.pprint(folders)

    if args.folder in folders:
        param = {
            "q": "'{0}' in parents and trashed = false".format(folders[args.folder]),
            "fields": "nextPageToken,files({0})".format(temporary_moments_utils.FILE_FIELDS),
            "orderBy": "name"
        }

        # Call the Drive v3 API
        files = temporary_moments_utils.retrieve_files(service, param)

        # Saves photo data as json to be read by Jekyll
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(files, f, ensure_ascii=False, indent=4)

        # TODO: Stop generating js file for data
        # Saves photo data as js variable to be read by js
        with open('data.js', 'w', encoding='utf-8') as f:
            f.write("var photos = {0}; export {{ photos }};".format(json.dumps(files, ensure_ascii=False, indent=2)))

    else:
        raise FileNotFoundError("{0} folder not found.".format(args.folder))

if __name__ == '__main__':
    main()