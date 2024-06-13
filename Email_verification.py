from flask import request, jsonify
from Email_send import send_reset_email
from models.Utilisateur import Utilisateur
from app import db
import app

import re

def is_valid_email(email):
    # Expression régulière pour vérifier le format de l'email
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


@app.route('/reset_password', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    email = data.get('email')
    
    # Vérifiez le format de l'email
    if not is_valid_email(email):
        return jsonify({"message": "Format d'email invalide"}), 400
    
    # Vérifiez si l'email existe dans la base de données
    user = Utilisateur.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"message": "Aucun utilisateur trouvé avec cet email"}), 404
    
    # Générer un token de réinitialisation (à implémenter)
    token = user.get_reset_password_token()  # Assurez-vous d'avoir cette méthode dans votre modèle Utilisateur

    # Envoyer l'email avec le lien de réinitialisation (à implémenter)
    send_reset_email(user, token)  # Implémentez la fonction d'envoi d'email
    
    return jsonify({"message": "Si un compte avec cet email existe, un email a été envoyé avec des instructions pour réinitialiser le mot de passe."})
