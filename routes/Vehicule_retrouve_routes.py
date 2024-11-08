# routes/vehicule_retrouve_routes.py
from flask import Blueprint, request, jsonify
from app import db
from models.Vehicule_retrouve import VehiculeRetrouve
from flask_login import login_required, current_user
from datetime import datetime

vehicule_retrouve_bp = Blueprint('vehicule_retrouve_bp', __name__)
@vehicule_retrouve_bp.route('/vehiculeRetrouve', methods=['POST'])

def enregistrer_vehicule_retrouve():
    data = request.get_json()
    
    # Validation des champs obligatoires
    missing_fields = [field for field in [
        'nomRetrouveur', 'prenomRetrouveur', 'numPlaque', 
        'lieuLong', 'lieuLat', 'marque', 'modele', 'dateHeure'
    ] if field not in data]

    if missing_fields:
        return jsonify({"message": f"Champs manquants : {', '.join(missing_fields)}"}), 400

    try:
        date_heure = datetime.strptime(data['dateHeure'], '%Y-%m-%d %I:%M %p')

        
        vehicule_retrouve = VehiculeRetrouve(
            utilisateur_id=current_user.id,
            nom_retrouveur=data['nomRetrouveur'],
            prenom_retrouveur=data['prenomRetrouveur'],
            num_plaque=data['numPlaque'],
            lieu_long=data['lieuLong'],
            lieu_lat=data['lieuLat'],
            marque=data['marque'],
            modele=data['modele'],
            date_heure=date_heure
        )
        
        db.session.add(vehicule_retrouve)
        db.session.commit()
        
        return jsonify({"message": "Véhicule retrouvé enregistré avec succès!", "data": vehicule_retrouve.to_dict()}), 201
    except ValueError as e:
        return jsonify({"message": f"Erreur de format de date : {e}"}), 400
    except Exception as e:
        return jsonify({"message": f"Une erreur est survenue : {e}"}), 500
