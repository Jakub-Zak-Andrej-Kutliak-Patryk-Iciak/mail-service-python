import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    APP_NAME = os.environ.get('APP_NAME', 'The Mail App')

    MQ_URL = os.getenv('MQ_URL', 'amqp://guest:guest@localhost:5672')
    MQ_QUEUE_NAME = os.environ.get('MQ_QUEUE_NAME', 'mail-queue')
    MQ_CONSUMER_TAG = os.environ.get('MQ_CONSUMER_TAG', 'mail-service-consumer')

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'google.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', '465')
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'True')
    # MAIL_DEBUG = os.environ.get('MAIL_DEBUG')
    MAIL_USERNAME = os.environ.get('MAIL_USER')
    MAIL_PASSWORD = os.environ.get('MAIL_PASS')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_DEFAULT_RECEIVER = os.environ.get('MAIL_DEFAULT_RECEIVER')
    # MAIL_MAX_EMAILS = os.environ.get('MAIL_MAX_EMAILS')
    # MAIL_SUPPRESS_SEND = os.environ.get('MAIL_SUPPRESS_SEND')
    # MAIL_ASCII_ATTACHMENTS = os.environ.get('MAIL_ASCII_ATTACHMENTS')
