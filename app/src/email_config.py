from flask_mail import Message
from flask_mailman import Mail
from app import mail

def create_mail(sender, recipients, message):
    msg = Message("Hello, ",
                    sender=sender,
                    recipients=recipients)
                    # ["to@examples.com"])
    msg.body = "Please click the following link to verify your account:" + message
    mail.send(msg)

