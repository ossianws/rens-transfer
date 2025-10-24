from flask import Flask





def create_app():
    app = Flask(__name__)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app









#run locally
if __name__ == '__main__':
    app.run(debug=True)
