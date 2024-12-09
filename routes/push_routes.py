from flask import Blueprint, request, jsonify
import requests
from models import OneSignalPlayerId
from app import db

push_bp = Blueprint('push_bp', __name__)

ONESIGNAL_API_KEY = "YOUR_ONESIGNAL_API_KEY"
ONESIGNAL_APP_ID = "6465087a-45b0-495c-b697-5fd3e057a45b"

@push_bp.route('/sendNotification', methods=['POST'])
def envoyer_notification_push():
    """
    Endpoint pour envoyer une notification push via OneSignal.
    """
    try:
        data = request.get_json()
        player_id = data.get('playerId')  # Player ID du destinataire
        titre = data.get('title')
        message = data.get('message')

        if not player_id or not titre or not message:
            return jsonify({"success": False, "error": "Champs manquants."}), 400

        # Préparer la requête pour OneSignal
        notification_data = {
            "app_id": ONESIGNAL_APP_ID,
            "include_player_ids": [player_id],
            "headings": {"en": titre},
            "contents": {"en": message},
        }

        # Envoyer la requête POST à OneSignal
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Basic {ONESIGNAL_API_KEY}",
        }
        response = requests.post(
            "https://onesignal.com/api/v1/notifications",
            headers=headers,
            json=notification_data,
        )

        if response.status_code == 200:
            return jsonify({"success": True, "response": response.json()}), 200
        else:
            return jsonify({"success": False, "error": response.json()}), response.status_code

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@push_bp.route('/api/enregistrer_player_id', methods=['POST'])
def enregistrer_player_id():
    """
    Endpoint pour enregistrer ou mettre à jour un Player ID OneSignal pour un utilisateur.
    """
    data = request.json

    utilisateur_id = data.get('utilisateurId')
    player_id = data.get('playerId')

    if not utilisateur_id or not player_id:
        return jsonify({"error": "Données manquantes : utilisateurId et playerId sont requis."}), 400

    try:
        # Vérifier si un Player ID existe déjà pour cet utilisateur
        player_id_existant = OneSignalPlayerId.query.filter_by(utilisateur_id=utilisateur_id).first()

        if player_id_existant:
            player_id_existant.player_id = player_id  # Met à jour le Player ID existant
        else:
            # Ajouter un nouveau Player ID
            nouveau_player_id = OneSignalPlayerId(utilisateur_id=utilisateur_id, player_id=player_id)
            db.session.add(nouveau_player_id)

        db.session.commit()
        return jsonify({"message": "Player ID enregistré ou mis à jour avec succès."}), 201

    except Exception as e:
        db.session.rollback()  # Annuler les modifications en cas d'erreur
        return jsonify({"error": f"Erreur interne du serveur : {str(e)}"}), 500


@push_bp.route('/api/getPlayerId/<int:utilisateur_id>', methods=['GET'])
def obtenir_player_id(utilisateur_id):
    """
    Endpoint pour récupérer le Player ID d'un utilisateur spécifique.
    """
    try:
        player_id = OneSignalPlayerId.query.filter_by(utilisateur_id=utilisateur_id).first()

        if player_id:
            return jsonify({"playerId": player_id.player_id}), 200
        else:
            return jsonify({"error": "Aucun Player ID trouvé pour cet utilisateur."}), 404

    except Exception as e:
        return jsonify({"error": f"Erreur interne du serveur : {str(e)}"}), 500
