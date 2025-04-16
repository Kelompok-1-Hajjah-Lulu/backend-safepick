from dotenv import load_dotenv

load_dotenv(".env.staging")

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from .config import Config


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)

    from .routes import main

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
