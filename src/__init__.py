from flask import Flask
from flasgger import Swagger

from config import Config
from src.services import EmailService, MQService
from src.api.routes import register_routes

mail = EmailService()
messageQueue = MQService()


def create_app(config_class=Config):
    app = Flask(__name__)
    swagger = Swagger(app)
    app.config.from_object(Config)
    register_routes(app)
    mail.init_app(app)

    messageQueue.init_mq(host=Config.MESSAGE_QUEUE_HOST, queue_name=Config.MESSAGE_QUEUE_NAME)
    messageQueue.on_message_callback(mail.send_mail)

    return app
