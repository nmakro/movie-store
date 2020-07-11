import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import configMap

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app_config = configMap[os.getenv("ENV_TYPE", default="PROD_ENV")]

    app.config.from_object(app_config)
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate = Migrate(app, db)

    from app.model.users import User
    from app.model.movies import Movie

    from .api import bp

    app.register_blueprint(bp, url_prefix="/api/v1")

    return app
