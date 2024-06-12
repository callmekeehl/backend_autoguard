from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from models.Utilisateur import Utilisateur
from app import db

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('motDePasse')

    user = Utilisateur.query.filter_by(email=email).first()
    
    if user and user.verify_password(password):
        login_user(user)
        return jsonify({"message": "Connexion réussie", "utilisateurId": user.utilisateurId, "type": user.type}), 200
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
