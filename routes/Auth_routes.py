from flask_login import current_user, login_required, login_user, logout_user
import jwt
import datetime
from flask import Blueprint, current_app, jsonify, request

from models import Utilisateur

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('motDePasse')

    user = Utilisateur.query.filter_by(email=email).first()
    
    if user and user.verify_password(password):
        login_user(user)

        # Générer un token JWT
        token = jwt.encode({
            'user_id': user.utilisateurId,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # Token expire dans 24 heures
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        # Retourner le token dans la réponse JSON
        return jsonify({
            "message": "Connexion réussie",
            "utilisateurId": user.utilisateurId,
            "type": user.type,
            "token": token
        }), 200
    else:
        return jsonify({"message": "Email ou Mot de passe invalide"}), 401

@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Deconnexion réussie"}), 200

@auth_bp.route('/current_user', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify(current_user.to_dict())
    else:
        return jsonify({"message": "Pas d'utilisateur connecté"}), 401
