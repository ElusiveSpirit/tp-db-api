import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'asdq3dwdwedasdfq34frewf3qf'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'},
    {'name': 'VK', 'url': 'http://www.VKontakteID.ru/<username>'}
]

# DB options
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASE_DIR, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True


# mail server settings
# Debug server for console:
#   python -m smtpd -n -c DebuggingServer localhost:25
# Solution for production https://mailcatcher.me/

MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['you@example.com']
