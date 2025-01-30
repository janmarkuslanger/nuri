import os

UPLOAD_FOLDER = "uploads"
SQLALCHEMY_DATABASE_URI = "sqlite:///nuri.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.urandom(24)