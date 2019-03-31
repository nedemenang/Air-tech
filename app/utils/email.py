from flask_mail import Message
from flask import render_template
from app import mail, app
from threading import Thread


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, flight, flight_seat, user, ticket):
        msg = Message(subject, sender=sender, recipients=recipients)

        msg.html = render_template('flight_email.html', flight=flight, flight_seat=flight_seat, user=user, ticket=ticket)

        msg.body = render_template('flight_email.txt', flight=flight, flight_seat=flight_seat, user=user, ticket=ticket)

        Thread(target=send_async_email, args=(app, msg)).start()