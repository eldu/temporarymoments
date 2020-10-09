# Instructions

## Updating the photo database
Basically, I run a script that queries Google Drive for the photos. Then it saves metadata about those photos into 
[photos.json](_data/photos.json). This data is then used to build the website.

1. Add photos to the Google Drive folder for temporary moments
1. Run `python get_photos.py` with a credentials file. It creates a `photos.json` file.
1. Build
  - `npm run build` or `bundle exec jekyll build`
1. Test locally
  - `npm start` or `bundle exec jekyll serve`
1. Deploy
  - `npm run deploy`