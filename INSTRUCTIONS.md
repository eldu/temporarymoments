# Instructions

## Photo Specifications

Final Photo for display
- Fit Dimensions: 2560 x 1440 px
- Aspect Ratio: 16:9
- File size recommended <= 500 kb. Max is 20 mb.
- .png or .jpg

## Updating the photo database
Basically, I run a script that queries Google Drive for the photos. Then it saves metadata about those photos into 
[photos.json](_data/photos.json). This data is then used to build the website.

1. Add photos to the Google Drive folder for temporary moments
1. Run `python update_photos.py` with a credentials file. It creates a `photos.json` file.
1. Build and test locally
    - `npm run develop`
1. Push to Master
1. Deploy
    - `npm run deploy`