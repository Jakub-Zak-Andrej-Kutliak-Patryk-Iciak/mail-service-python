from typing import Optional

from flask_mail import Mail, Message

from config import Config
from src.models import Singleton


class EmailService(metaclass=Singleton):

    def __init__(self, app=None):
        self.mail = Mail(app)

    def init_app(self, app):
        self.mail = Mail(app)

    def __check_mail_present(self):
        if self.mail is None:
            raise Exception("Mail service not linked to the app")

    def send_mail_with_sender(self, message: Message, sender: str) -> None:
        self.__check_mail_present()
        message.sender = sender
        self.send_mail(message)

    def send_mail(self, message: Message) -> None:
        if not message:
            print("Message was not provided!")
        else:
            self.mail.send(message)

    @staticmethod
    def parse_request_to_message(request: dict) -> tuple[Message, Optional[str]]:
        override_email = Config.MAIL_DEFAULT_RECEIVER
        sender = Config.MAIL_DEFAULT_SENDER
        missing = []
        receiver = request.get('receiver')
        subject = request.get('subject')
        message = request.get('message')

        if receiver is None:
            missing.append('receiver')
        if subject is None:
            missing.append('subject')
        if message is None:
            missing.append('message')

        error = f"Missing required parameters: {missing}" if len(missing) > 0 else None
        return Message(
            recipients=[override_email if override_email else receiver],
            sender=(Config.APP_NAME, sender),
            subject=subject,
            body=message,
        ), error
