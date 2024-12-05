# routes/vehicule_retrouve_routes.py
from flask import Blueprint, request, jsonify
from app import db
from models.MotifRdv import MotifRdv
from models.Vehicule_retrouve import VehiculeRetrouve
from flask_login import login_required, current_user
from datetime import datetime

vehicule_retrouve_bp = Blueprint('vehicule_retrouve_bp', __name__)

@vehicule_retrouve_bp.route('/vehiculeRetrouveAvecRdv', methods=['POST'])


def enregistrer_vehicule():
    data = request.get_json()

    try:
        # Extraire utilisateurId de motifData
        utilisateur_id = data.get('motifData', {}).get('utilisateurId')
        motif_data = data.get('motifData', {})

        if utilisateur_id is None:
            return jsonify({"error": "Utilisateur ID est manquant dans motifData"}), 400
        

        vehicule = VehiculeRetrouve(
            utilisateur_id=utilisateur_id,
            nom_retrouveur=data['nomRetrouveur'],
            prenom_retrouveur=data['prenomRetrouveur'],
            num_plaque=data['numPlaque'],
            lieu_long=data['lieuLong'],
            lieu_lat=data['lieuLat'],
            marque=data['marque'],
            modele=data['modele'],
            date_heure=data['dateHeure'],
            quartier=data.get('quartier', '')
        )

        db.session.add(vehicule)
        db.session.commit()

        
        # Enregistrer le rendez-vous (motif)
        motif_description = motif_data.get('motifDescription')
        date = motif_data.get('date')

        if not motif_description or not date:
            return jsonify({"error": "Données manquantes pour créer un rendez-vous"}), 400
        try:
            date_obj = datetime.fromisoformat(date)
        except ValueError:
            return jsonify({"error": "Format de date invalide"}), 400

        motif_rdv = MotifRdv(
            utilisateurId=utilisateur_id,
            motifDescription=motif_description,
            date=date_obj
        )
        db.session.add(motif_rdv)
        db.session.commit()

        return jsonify({"message": "Véhicule retrouvé et rendez-vous enregistré avec succès."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400