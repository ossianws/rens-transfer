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

    from app.models import User, Graph
    from app.db_init import populate_db,empty_db, create_generator_dict
    from app.users import user_list

    

    admin_user = User(user_list["1"]["username"])
    admin_user.set_hash(user_list["1"]["password_hash"])
    app.config['ADMIN_USER'] = admin_user

   
    from app.errors import error_bp
    app.register_blueprint(error_bp)

    from app.graphs import bp
    app.register_blueprint(bp)



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

    

    app.logger.info('App startup')
    
    
    @app.cli.command("reset-db")
    def reset_db():
        """Empty and repopulate the database."""
        with app.app_context():
            from app.db_init import populate_db, empty_db, create_generator_dict
            empty_db(db)
            populate_db(create_generator_dict(), db)
            print("Database cleared and repopulated.")
    
    @app.cli.command("regenerate-csv")
    def regenerate_csv():
        """Re-clean data from CSV files """
        from app.data_cleaning import clean_activities_updated, clean_organisations, clean_meetings
        
        raw_dir = app.config['RAW_CSV_FOLDER'] or os.join(os.path.dirname(os.path.abspath(__file__)),'datasets/raw')
        dest_dir = app.config['PROCESSED_CSV_FOLDER'] or os.join(os.path.dirname(os.path.abspath(__file__),'datasets/processed'))
            
        for cleaner_function in [clean_activities_updated,clean_organisations,clean_meetings]:
            df, filename = cleaner_function(raw_dir)
            filepath = os.path.join(dest_dir,filename)
            df.to_csv(filepath,index=False)
            print(f'DF saved to {filepath}')
            
        print(f'Finished. Processed data can be found at {dest_dir}')
    
    return app

from app import models






