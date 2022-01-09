import json

from flask_mail import Message
from flask import Blueprint, request, jsonify, abort, Response

from src.services import EmailService

v1 = Blueprint('v1', __name__, url_prefix='/v1')

email_service = EmailService()


@v1.route('/user/register/confirm', methods=['POST'])
def send_register_confirmation():
    name = request.get_json().get('name')
    if name is None:
        abort(400, "'name' parameter not found")
    email = request.get_json().get('email')
    if email is None:
        abort(400, "'email' parameter not found")
    message = Message(
        recipients=[email],
        subject="Welcome to The Parking App",
        body=f"Hi {name}, we are very happy you decided to join us!",
    )
    email_service.send_mail(message)
    return jsonify({"success": True})


@v1.route('/send', methods=['POST'])
def send_email():
    receiver = request.get_json().get('receiver')
    if receiver is None:
        abort(400, "Required parameter 'receiver' parameter not found")
    subject = request.get_json().get('subject')
    if subject is None:
        abort(400, "Required parameter 'subject' parameter not found")
    message = request.get_json().get('message')
    if message is None:
        abort(400, "Required parameter 'message' parameter not found")
    message = Message(
        recipients=[receiver],
        subject=subject,
        body=message,
    )
    sender = request.get_json().get('sender')
    if sender:
        message.sender = sender
    email_service.send_mail(message)
    return jsonify({"success": True})


@v1.errorhandler(400)
def error_handler(error: any) -> Response:
    return Response(json.dumps({'error': error.description}), status=400, mimetype='application/json')


@v1.errorhandler(Exception)
def unhandled_error(error: any) -> Response:
    print("An error occurred => " + str(error))
    return Response(json.dumps({'error': 'UPS! Something went wrong :('}), status=500, mimetype='application/json')
