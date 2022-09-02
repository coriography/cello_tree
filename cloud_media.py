# Set Cloudinary credentials
from dotenv import load_dotenv

load_dotenv()

import cloudinary
import cloudinary.uploader
import cloudinary.api
import json

# Return "https" URLs
config = cloudinary.config(secure=True)

# Log the configuration
# ==============================
print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")


def upload_image(file):
    """Upload the image and get its URL."""

    upload_info = cloudinary.uploader.upload(file, unique_filename=False, overwrite=True)
    cloudinary.CloudinaryImage("quickstart_butterfly").image(radius="max", effect="sepia")
    # TODO: set the public_id param to cellist name or ID?

    # Build the URL for the image and save it in the variable 'srcURL'
    # src_url = cloudinary.CloudinaryImage(cellist_id).build_url()

    # Log the image URL to the console.
    # Copy this URL in a browser tab to generate the image on the fly.
    # print("****2. Upload an image****\nDelivery URL: ", src_url, "\n")


# def get_asset_info():
#     # Get and use details of the image
#     # ==============================
#     print('in get_asset_info()')
#
#     # Get image details and save it in the variable 'image_info'.
#     image_info = cloudinary.api.resource(cellist_id)
#     print("****3. Get and use details of the image****\nUpload response:\n", json.dumps(image_info, indent=2), "\n")
#
#
# def create_image_tag():
#     # Transform the image
#     # ==============================
#
#     # Create an image tag with transformations applied to the src URL.
#     imageTag = cloudinary.CloudinaryImage("quickstart_butterfly").image(radius="max", effect="sepia")
#
#     # Log the image tag to the console
#     print("****4. Transform the image****\nTransfrmation URL: ", imageTag, "\n")
#
#
# def main():
#     upload_image('static/img/add_cellist.png')
#     get_asset_info()
#     create_image_tag()
#
#
# main()
