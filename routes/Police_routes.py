import datetime
from flask import Blueprint, current_app, request, jsonify
import jwt
from models.Police import Police
from models.Utilisateur import Utilisateur
from app import db

police_bp = Blueprint('police_bp', __name__)

@police_bp.route('/polices', methods=['POST'])
def create_police():
    data = request.get_json()

    print("Données JSON reçues:", data)

    required_fields = ['nom', 'prenom', 'email', 'adresse', 'telephone', 'motDePasse', 'nomDepartement', 'adresseDepartement']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({"error": f"Les champs suivants sont manquants ou vides: {', '.join(missing_fields)}"}), 400

    if Utilisateur.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Un utilisateur avec cet email existe déjà."}), 400

    try:
        # Créez l'utilisateur et assignez directement le type 'police'
        new_police = Police(
            nom=data['nom'],
            prenom=data['prenom'],
            email=data['email'],
            adresse=data['adresse'],
            telephone=data['telephone'],
            type='police', 
            nomDepartement=data['nomDepartement'],
            adresseDepartement=data['adresseDepartement']
        )
        new_police.motDePasse = data['motDePasse']

         # Enregistrer le token FCM si fourni
        fcm_token = data.get('fcm_token')
        if fcm_token:
            new_police.fcm_token = fcm_token


        db.session.add(new_police)
        db.session.commit()  # Commit ici pour persister les changements
        
        # Générez un jeton JWT pour le nouveau compte police
        token = jwt.encode({
            'police_id': new_police.utilisateurId,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Expire dans 1 heure
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        # Inclure le jeton et les informations du compte dans la réponse
        response_data = {
            "message": "Police créé",
            "policeId": new_police.policeId,
            "access_token": token,
            "police": new_police.to_dict()
        }

        return jsonify(response_data), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@police_bp.route('/polices', methods=['GET'])
def get_polices():
    polices = Police.query.all()
    return jsonify([p.to_dict() for p in polices])

@police_bp.route('/polices/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_police(id):
    police = Police.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(police.to_dict())

    if request.method == 'PUT':
        data = request.get_json()

        police.nom = data.get('nom', police.nom)
        police.prenom = data.get('prenom', police.prenom)
        police.email = data.get('email', police.email)
        police.adresse = data.get('adresse', police.adresse)
        police.telephone = data.get('telephone', police.telephone)
        police.nomDepartement = data.get('nomDepartement', police.nomDepartement)
        police.adresseDepartement = data.get('adresseDepartement', police.adresseDepartement)

        if 'motDePasse' in data:
            police.motDePasse = data['motDePasse']  # Utiliser le setter pour mettre à jour le mot de passe hashé

        db.session.commit()
        return jsonify({"message": "Police mise à jour"})

    if request.method == 'DELETE':
        try:
            db.session.delete(police)
            db.session.commit()
            return jsonify({"message": "Police supprimée"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


@police_bp.route('/polices/<int:id>/token', methods=['POST'])
def store_fcm_token(id):
    police = Police.query.get_or_404(id)
    fcm_token = request.json.get('fcm_token')
    
    if fcm_token:
        police.fcm_token = fcm_token
        db.session.commit()
        return jsonify({"message": "Token FCM enregistré avec succès"}), 200
    else:
        return jsonify({"error": "Token FCM manquant"}), 400
