from flask import Blueprint, request, jsonify
from models.Garage import Garage
from models.Utilisateur import Utilisateur
from app import db

garage_bp = Blueprint('garage_bp', __name__)


@garage_bp.route('/garages', methods=['POST'])
def create_garage():
    data = request.get_json()

    print("Données JSON reçues:", data)

    required_fields = ['nom', 'prenom', 'email', 'adresse', 'telephone', 'motDePasse', 'nomGarage', 'adresseGarage']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({"error": f"Les champs suivants sont manquants ou vides: {', '.join(missing_fields)}"}), 400

    if Utilisateur.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Un utilisateur avec cet email existe déjà."}), 400

    try:
        # Créez l'utilisateur et assignez directement le type 'garage'
        new_garage = Garage(
            nom=data['nom'],
            prenom=data['prenom'],
            email=data['email'],
            adresse=data['adresse'],
            telephone=data['telephone'],
            type='garage',  # Utilisez le polymorphic_identity 'garage'
            nomGarage=data['nomGarage'],
            adresseGarage=data['adresseGarage']
        )
        new_garage.motDePasse = data['motDePasse']
        db.session.add(new_garage)
        db.session.commit()  # Commit ici pour persister les changements

        return jsonify({"message": "Garage créé", "garageId": new_garage.garageId}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@garage_bp.route('/garages', methods=['GET'])
def get_garages():
    garages = Garage.query.all()
    return jsonify([g.to_dict() for g in garages])


@garage_bp.route('/garages/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_garage(id):
    garage = Garage.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(garage.to_dict())

    if request.method == 'PUT':
        data = request.get_json()

        garage.nom = data.get('nom', garage.nom)
        garage.prenom = data.get('prenom', garage.prenom)
        garage.email = data.get('email', garage.email)
        garage.adresse = data.get('adresse', garage.adresse)
        garage.telephone = data.get('telephone', garage.telephone)
        garage.nomGarage = data.get('nomGarage', garage.nomGarage)
        garage.adresseGarage = data.get('adresseGarage', garage.adresseGarage)

        if 'motDePasse' in data:
            garage.motDePasse = data['motDePasse']  # Utiliser le setter pour mettre à jour le mot de passe hashé

        db.session.commit()
        return jsonify({"message": "Garage mis à jour"})

    if request.method == 'DELETE':
        try:
            db.session.delete(garage)
            db.session.commit()
            return jsonify({"message": "Garage supprimé"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500