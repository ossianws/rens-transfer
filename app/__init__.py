from flask import Flask
from config import Config




def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    import logging
    logging.basicConfig(filename='global.log',level=logging.DEBUG)

    handler = logging.FileHandler('global.log')
    app.logger.addHandler(handler)
    
    
    return app










