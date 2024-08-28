import os
from flask import current_app

def save_file(file, folder):
    filename = file.filename
    file_path = os.path.join(current_app.config[folder], filename)
    file.save(file_path)
    return file_path

def create_folders():
    if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
        os.makedirs(current_app.config['UPLOAD_FOLDER'])
    if not os.path.exists(current_app.config['RESULT_FOLDER']):
        os.makedirs(current_app.config['RESULT_FOLDER'])
