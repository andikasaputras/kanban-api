import os

from dotenv import load_dotenv
from flask import Flask

from config import config
from .db import init_db
from logging_config import init_logging
from .exceptions.errorhandlers import init_errorhandlers
from .auth.auth_routes import auth


def create_app(config_name=None):
    # Load environment variables from .env file
    load_dotenv()
    ENV = os.getenv("ENV")

    app = Flask(__name__)
    config_class = config[config_name] if config_name else config[ENV]
    app.config.from_object(config_class)

    # Initialize Flask extensions
    init_db(app)
    init_logging(app)
    init_errorhandlers(app)

    # Register blueprints
    app.register_blueprint(auth, url_prefix="/auth")

    return app
