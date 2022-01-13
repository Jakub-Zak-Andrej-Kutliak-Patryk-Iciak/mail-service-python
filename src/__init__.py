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

    messageQueue.init_mq(connect_url=Config.RABBITMQ_URL_PARAMS,
                         queue_name=Config.RABBITMQ_QUEUE_NAME,
                         consumer_tag=Config.RABBITMQ_CONSUMER_TAG,
                         on_message_callback=mail.send_mail,
                         app=app)

    return app
