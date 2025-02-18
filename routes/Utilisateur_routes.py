import datetime
from flask import Blueprint, current_app, request, jsonify
from flask_login import login_required
import jwt
from models import Declaration, Notification, Rdv, Police, Garage
from models.Utilisateur import Utilisateur
from app import db

utilisateur_bp = Blueprint('utilisateur_bp', __name__)


# Utilisateur routes
@utilisateur_bp.route('/utilisateurs', methods=['GET', 'POST'])
def handle_utilisateurs():
    if request.method == 'POST':
        data = request.get_json()

        # Vérifie si l'email existe déjà
        if Utilisateur.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Un utilisateur avec cet email existe déjà."}), 400
        
        
        new_user = Utilisateur(
            nom=data['nom'],
            prenom=data['prenom'],
            email=data['email'],
            adresse=data['adresse'],
            telephone=data['telephone']
        )
        new_user.motDePasse = data['motDePasse']

         # Enregistrer le token FCM si fourni
        fcm_token = data.get('fcm_token')
        if fcm_token:
            new_user.fcm_token = fcm_token


        db.session.add(new_user)
        db.session.commit()

        # Génération d'un jeton JWT pour le nouvel utilisateur
        token = jwt.encode({
            'user_id': new_user.utilisateurId,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expire dans 1 heure
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({"message": "Utilisateur créé", "access_token": token,"user_id": new_user.utilisateurId, "user": new_user.to_dict()}), 201
    
        

    if request.method == 'GET':
        utilisateurs = Utilisateur.query.all()
        return jsonify([u.to_dict() for u in utilisateurs])


@utilisateur_bp.route('/utilisateurs/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(utilisateur.to_dict())

    if request.method == 'PUT':
        data = request.get_json()
        utilisateur.nom = data['nom']
        utilisateur.prenom = data['prenom']
        utilisateur.email = data['email']
        utilisateur.adresse = data['adresse']
        utilisateur.telephone = data['telephone']
        if 'motDePasse' in data:
            utilisateur.motDePasse = data['motDePasse']  # Utiliser le setter pour hacher le mot de passe
        db.session.commit()
        return jsonify({"message": "Utilisateur mis à jour"})

    if request.method == 'DELETE':
        db.session.delete(utilisateur)
        db.session.commit()
        return jsonify({"message": "Utilisateur supprimé"})
    
@utilisateur_bp.route('/utilisateurs/<int:id>', methods=['GET'])
def get_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    return jsonify({
        'nom': utilisateur.nom,
        'prenom': utilisateur.prenom,
        'utilisateurId': utilisateur.utilisateurId
    })

@utilisateur_bp.route('/utilisateurs/<int:id>/token', methods=['POST'])
def store_fcm_token(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    fcm_token = request.json.get('fcm_token')
    
    if fcm_token:
        utilisateur.fcm_token = fcm_token
        db.session.commit()
        return jsonify({"message": "Token FCM enregistré avec succès"}), 200
    else:
        return jsonify({"error": "Token FCM manquant"}), 400
