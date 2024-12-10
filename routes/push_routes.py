from flask import Blueprint, request, jsonify
import requests
from models import FcmToken
from app import db

push_bp = Blueprint('push_bp', __name__)

FCM_SERVER_KEY = "YOUR_FCM_SERVER_KEY"

@push_bp.route('/sendNotification', methods=['POST'])
def envoyer_notification_push():
    """
    Endpoint pour envoyer une notification push via FCM à un utilisateur simple.
    """
    try:
        data = request.get_json()
        utilisateur_id = data.get('utilisateurId')  # ID de l'utilisateur destinataire
        titre = data.get('title')  # Titre de la notification
        message = data.get('message')  # Message de la notification

        if not utilisateur_id or not titre or not message:
            return jsonify({"success": False, "error": "Champs manquants."}), 400

        # Récupérer le token FCM de l'utilisateur
        token = FcmToken.query.filter_by(utilisateur_id=utilisateur_id).first()

        if not token:
            return jsonify({"success": False, "error": "Token FCM non trouvé pour cet utilisateur."}), 404

        # Créer le message de notification
        notification_data = {
            "notification": {
                "title": titre,
                "body": message
            },
            "to": token.fcm_token  # Token FCM de l'utilisateur cible
        }

        # Envoi de la notification via FCM
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"key={FCM_SERVER_KEY}"
        }

        response = requests.post(
            "https://fcm.googleapis.com/fcm/send",
            headers=headers,
            json=notification_data
        )

        if response.status_code == 200:
            return jsonify({"success": True, "response": response.json()}), 200
        else:
            return jsonify({"success": False, "error": response.json()}), response.status_code

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@push_bp.route('/enregistrer_token_fcm', methods=['POST'])
def enregistrer_token_fcm():
    """
    Endpoint pour enregistrer ou mettre à jour un token FCM pour un utilisateur.
    """
    data = request.json

    utilisateur_id = data.get('utilisateurId')
    fcm_token = data.get('fcmToken')

    if not utilisateur_id or not fcm_token:
        return jsonify({"error": "Données manquantes : utilisateurId et fcmToken sont requis."}), 400

    try:
        # Vérifier si un token FCM existe déjà pour cet utilisateur
        token_existant = FcmToken.query.filter_by(utilisateur_id=utilisateur_id).first()

        if token_existant:
            token_existant.fcm_token = fcm_token  # Met à jour le token existant
        else:
            # Ajouter un nouveau token
            nouveau_token = FcmToken(utilisateur_id=utilisateur_id, fcm_token=fcm_token)
            db.session.add(nouveau_token)

        db.session.commit()
        return jsonify({"message": "Token FCM enregistré ou mis à jour avec succès."}), 201

    except Exception as e:
        db.session.rollback()  # Annuler les modifications en cas d'erreur
        return jsonify({"error": f"Erreur interne du serveur : {str(e)}"}), 500
