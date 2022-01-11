import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # comment out to preserve default
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
    # MAIL_DEBUG = os.environ.get('MAIL_DEBUG')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    # MAIL_MAX_EMAILS = os.environ.get('MAIL_MAX_EMAILS')
    # MAIL_SUPPRESS_SEND = os.environ.get('MAIL_SUPPRESS_SEND')
    # MAIL_ASCII_ATTACHMENTS = os.environ.get('MAIL_ASCII_ATTACHMENTS')
    MESSAGE_QUEUE_HOST = os.environ.get('MESSAGE_QUEUE_HOST')
    MESSAGE_QUEUE_NAME = os.environ.get('MESSAGE_QUEUE_NAME')
