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

    if user:
        print(f"User found: {user.nom} - Type: {user.type}")
        if user.verify_password(password):
            print("Password verified")

            login_user(user)
            print("User logged in")

            # Générer un token JWT
            token = jwt.encode({
                'user_id': user.utilisateurId,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, current_app.config['SECRET_KEY'], algorithm='HS256')

            print("JWT generated")

            # Préparer les données en fonction du type d'utilisateur
            if user.type == 'garage':
                user_data = {
                    "utilisateurId": user.utilisateurId,
                    "type": user.type,
                    "nom": user.nom,
                    "prenom": user.prenom,
                    "email": user.email,
                    "adresse": user.adresse,
                    "telephone": user.telephone,
                    "nomGarage" : user.nomGarage,
                    "adresseGarage" : user.adresseGarage,
                    "garageId": user.garageId
                }
            elif user.type == 'police':
                user_data = {
                    "utilisateurId": user.utilisateurId,
                    "type": user.type,
                    "nom": user.nom,
                    "prenom": user.prenom,
                    "email": user.email,
                    "adresse": user.adresse,
                    "telephone": user.telephone,
                    "nomDepartement" : user.nomDepartement,
                    "adresseDepartement" : user.adresseDepartement,
                    "policeId": user.policeId
                }
            else:  # Utilisateur normal
                user_data = {
                    "utilisateurId": user.utilisateurId,
                    "type": user.type,
                    "nom": user.nom,
                    "prenom": user.prenom,
                    "email": user.email,
                    "adresse": user.adresse,
                    "telephone": user.telephone
                }


            return jsonify({
                "message": "Connexion réussie",
                "token": token,
                "user": user_data
            }), 200
        else:
            print("Mot de passe Invalide")
    else:
        print("Utilisateur non trouvé")

    return jsonify({"message": "Email ou Mot de passe invalide"}), 401


@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Deconnexion réussie"}), 200

@auth_bp.route('/current_user', methods=['GET'])
@login_required
def get_current_user():
    if current_user.is_authenticated:
        return jsonify(current_user.to_dict())
    else:
        return jsonify({"message": "Pas d'utilisateur connecté"}), 401
