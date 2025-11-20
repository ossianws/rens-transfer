import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG') or 0
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/uploads')
    TESTING = 1
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    PASSWORD_HASH = os.environ.get('PASSWORD_HASH') or 'pbkdf2:sha256:600000$zc8tNa0LofcsJ0HF$2ffeaa047f6e24c2e4995ddbde44ab4b2355d46127e3db83d23c0c977e56f9e0'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    