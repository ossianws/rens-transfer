from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os



login = LoginManager()
login.login_view = 'main.login'
db = SQLAlchemy()
migrate = Migrate()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    from app.models import User
    from app.db_init import populate_db,empty_db, generators
    from app.users import user_list

    

    admin_user = User(user_list["1"]["username"])
    admin_user.set_hash(user_list["1"]["password_hash"])
    app.config['ADMIN_USER'] = admin_user

   
    from app.errors import error_bp
    app.register_blueprint(error_bp)



    import logging
    from logging.handlers import RotatingFileHandler

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

    with app.app_context():
        try:
            populate_db(generators,db)
        except:
            app.logger.warning('Exception caught - Database was not empty at initialisation.')
            if app.config['TESTING']:
                empty_db(db)
                populate_db(generators,db)

    app.logger.info('App startup')
    
    
    return app

#from app import models



