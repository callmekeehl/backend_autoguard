from flask import Blueprint, request, jsonify
from models.Utilisateur import Utilisateur
from flask_login import current_user, login_required
from app import db

verification_bp = Blueprint('verification_bp', __name__)


# Access verification route
@verification_bp.route('/admin_only')
@login_required
def admin_only():
    if current_user.role != 'admin':
        return jsonify({"message": "Accès refusé : Admins seulement"}), 403
    return jsonify({"message": "Bienvenue, admin!"})


# Password Reset request route
@verification_bp.route('/reset_password', methods=['POST'])
def reset_password_request():
    data = request.get_json()
    user = Utilisateur.query.filter_by(email=data['email']).first()
    if user:
        # Générer un token de réinitialisation
        token = user.get_reset_password_token()
        # Envoyer l'email avec le lien de réinitialisation
        send_reset_email(user, token)
    return jsonify({"message": "Si un compte avec cet email existe, un email a été envoyé avec des instructions pour réinitialiser le mot de passe."})


# Password reset route
@verification_bp.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    user = Utilisateur.verify_reset_password_token(token)
    if not user:
        return jsonify({"message": "Token invalide ou expiré"}), 400
    data = request.get_json()
    user.motDePasse = data['motDePasse']
    db.session.commit()
    return jsonify({"message": "Mot de passe mis à jour avec succès"})
