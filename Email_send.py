from flask import url_for
from flask_mail import Mail, Message

mail = Mail()

def send_reset_email(user, token):
    msg = Message('Réinitialisation de votre mot de passe',
                  sender='noreply@yourdomain.com',
                  recipients=[user.email])
    link = url_for('reset_password', token=token, _external=True)
    msg.body = f'Pour réinitialiser votre mot de passe, cliquez sur le lien suivant : {link}'
    mail.send(msg)
