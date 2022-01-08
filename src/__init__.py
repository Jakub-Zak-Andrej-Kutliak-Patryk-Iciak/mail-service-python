from flask import Flask
from flasgger import Swagger

from config import Config
from src.services import EmailService
from src.api.routes import register_routes

mail = EmailService()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    register_routes(app)
    mail.init_app(app)
    swagger = Swagger(app)
    return app
