from flask_mail import Mail, Message

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
        self.mail.send(message)
