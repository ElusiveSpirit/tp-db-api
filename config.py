import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WTF_CSRF_ENABLED = False

# DB options
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
