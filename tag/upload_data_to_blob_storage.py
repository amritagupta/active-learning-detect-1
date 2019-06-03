import csv, json, re, time
#import cv2
#import shutil
from pathlib import Path
from azure.storage.blob import BlockBlobService
import sys
# import os


# Allow us to import utils
config_dir = str(Path.cwd().parent / "utils")
if config_dir not in sys.path:
    sys.path.append(config_dir)
from config import Config
if len(sys.argv)<2:
    raise ValueError("Need to specify config file")
config_file = Config.parse_file(sys.argv[1])

# Connect to blob storage location
block_blob_service = BlockBlobService(account_name=config_file["AZURE_STORAGE_ACCOUNT"], account_key=config_file["AZURE_STORAGE_KEY"])
container_name = config_file["image_container_name"]
print(container_name)

# Upload images from local source to blob storage location 
image_source = Path(config_file["local_image_upload_location"])
user_folders = config_file["user_folders"]

if user_folders:
    for subfolder in sorted(image_source.iterdir(), key=lambda sf: str(sf.name).lower()):
        if subfolder.is_dir():
            subfolder_name = subfolder.name
            subfolder_images = [img for img in sorted(subfolder.iterdir(), key=lambda i: str(i.name).lower())]
            for img in subfolder_images:
                img_blob_name = subfolder_name+"/"+img.name
                block_blob_service.create_blob_from_path(container_name, img_blob_name, str(subfolder/img.name))
else:
    folder_name = image_source.name
    folder_images = [img for img in sorted(image_source.iterdir(), key=lambda i: str(i.name).lower())]

# tagging_location = Path(config_file["tagging_location"])
# vott_project_name = config_file["vott_project_name"]