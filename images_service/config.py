# images_service/config.py
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "uploads"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
