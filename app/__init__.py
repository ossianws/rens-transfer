from flask import Flask
from config import Config
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
import os
import logging


login = LoginManager()
login.login_view = 'main.login'



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    login.init_app(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    from app.models import User
    from app.users import user_list

    admin_user = User(user_list["1"]["username"])
    admin_user.set_hash(user_list["1"]["password_hash"])
    app.config['ADMIN_USER'] = admin_user

   
    from app.errors import error_bp
    app.register_blueprint(error_bp)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setLevel('INFO')
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s %(levelname)s: %(message)s '
                          '[in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)

    app.logger.setLevel('INFO')
    app.logger.info('App startup')
    
    
    return app





