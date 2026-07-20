import os
import shutil

from flask import current_app


def zone_upload_folder(zone_id):
    return os.path.join(current_app.config["UPLOAD_FOLDER"], str(zone_id))


def remove_zone_files(zone_id):
    folder = zone_upload_folder(zone_id)
    if os.path.isdir(folder):
        shutil.rmtree(folder)
