import os

class Config:
    SECRET_KEY = 'your_secret_key'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    RESULT_FOLDER = os.path.join(os.getcwd(), 'results')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload limit
