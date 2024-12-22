from flask import Blueprint, request, jsonify
import requests
from models import FcmToken
from app import db
from google.auth.transport.requests import Request
from google.oauth2 import service_account


push_bp = Blueprint('push_bp', __name__)

FCM_SERVER_KEY = "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC/fZBKslE+cfyGECCue2pMJIywYzBeyM+zWty+uNzVkl5qXgcIqJvHBylvXzzcbXTSQs9blpiZRD+AMRqvxmIGpBZOgDnntUy92YYsOYWkG3JroLxC/biPmlf8zqXzrLgIAMSyNdYGxS85qYDpafjJUt8th0KUt5U0J43Hw4uId3xxYNBDnd/jQzNx4GqCMbWTyeLfuuny4TAjvlso5HfOC0kx4qQt8xgQ4qxRvWg116CIJPT3qfiozSrMSfGA0gJnX5O4yAeLK37XXj0fjJY6pNkLk34je1m81WSZs6gBIyyBIsy9moVM/gl2gLoOU91NrrElTwhQZclP128g1TWxAgMBAAECggEAA8R4D7AqC9asR2r1aaY0W8kmtEKChurgHNqlyy7R6w9h9VyVbaTIY9MO2Qnm2NaVqZyQF3Cc3siwwyUalE8mSi31ezGBciVnNbkCfC5DJEAFMUh/sh9RzHZJ7HrLjKhfFCRuIKxEe+xqcHHJ5bQkpYYqE+tvjB0ZV2XyOSlUvnUqoorvtxvhXw85K8hGsRcJGODiNCJEFKn2UjX3zUzVFlP1k37aQol6aCI8BtN5xcfVEdPpvKETWWVuHkiJVFl74dppD7Q8ZZAx3AqURq2SQkMZFFaq8mSvc/qg/1XjTU6yT0qKiWFbzEmbfK2h6RtkIrK8RtSxM/US2+4FolM73QKBgQDp2Uvcaoc70NS70W7kdNFfMx0xtEMwzULUKeBGjU9oGtlIXlqhRzy2+bchnf+X5cJwbdxogwenhEX8ZsPkRTR7FsCKH52TuXnhkFJ3gnqSCwLgch/C3tZeTusp24m0Hh2s5gu+AfIvWcfDAZ9XTrDCdiq/5Cbod4nvNqhEHAYqAwKBgQDRoRnxvAXUDTsUHcshekVq7IgGYWrk/7pvoxZD7TdFympeVCQdJok98jur2Lq3e+FRmsh/AYRXZwEGB8Lh5NmPtLUsCt8Q3a/7VuvxM7bwFkSCVzBy0/IWLhZZpJ1MUX2Sv2nDvU5wtFAXOe3vkQn7GNx/QifW+O2PAlX4Zq0tOwKBgCufBiCimoFU7inu4lGpXNj2Tu7Tomj7EQlEmnpup65Su89dEmjdQf0bzcZuk5wBFukkBSZVstrTuL5haQ8uvaBsWRQq25kP0yV5Z3i1lSmi9jFp+HTAXpqO/Bz9v80ihQSYkP4rnMKqa7H7nn6Jxj0wD79lzsA0dD10I6U42QmDAoGBAIbM4OEYtmrAw0/RRNFXThJO3b20oUd2xs2JAwVVImjnm/TiiIKSSEikXwjHinH44FBY\nhztcn1yQ6RCWpxQZ1Glbm/EhYIX4+HRYVcq6JZZHy3BBXu9IKXFn24lzmI7+DBD0s69iKXHCEYqN/tpB2zgzqX7P7MyJMEH5D413gT8HAoGADoVBgobc5hpd0Isi0XrB\nIhNNm0W0mCtKntiPPKLZNYTL8+37P/5u7DHg1t4Om4Cex0o+rPVBs0vCz9HE62Yr\nqQScn4XX5r3dJdORK71+RoGm6mNSbrtS/XSxPVtAjOSGSS0+8RgB72kj9AxaFvZU3YMSgwBc+U/+l4KWgCFDHbQ="

push_bp = Blueprint('push_bp', __name__)
def get_oauth_token():
    """
    Génère un token OAuth 2.0 pour l'API FCM v1.
    """
    try:
        # Chemin vers clé JSON du compte de service
        SERVICE_ACCOUNT_FILE = "config/serviceAccountKey.json"
        
        # Charger les informations du compte de service
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=["https://www.googleapis.com/auth/firebase.messaging"]
        )

        # Rafraîchir le token OAuth 2.0
        request = Request()
        credentials.refresh(request)
        return credentials.token

    except Exception as e:
        raise RuntimeError(f"Erreur lors de la génération du token OAuth : {str(e)}")


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

        # Générer le token OAuth 2.0
        try:
            oauth_token = get_oauth_token()
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
        

        # Créer le message de notification
        notification_data = {
            "message": {
                "token": token.fcm_token,  # token cible
                "notification": {
                    "title": titre,
                    "body": message
                },
                "android": {
                    "priority": "HIGH"
                }
            }
        }

        # Envoi de la notification via FCM
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {oauth_token}"
        }

        response = requests.post(
            "https://fcm.googleapis.com/v1/projects/autoguardflutter/messages:send",
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


@push_bp.route('/getFCMToken/<int:utilisateur_id>', methods=['GET'])
def get_fcm_token(utilisateur_id):
    """
    Endpoint pour récupérer le token FCM d'un utilisateur.
    """
    try:
        token = FcmToken.query.filter_by(utilisateur_id=utilisateur_id).first()

        if token:
            return jsonify({"fcmToken": token.fcm_token}), 200
        else:
            return jsonify({"error": "Token FCM non trouvé pour cet utilisateur."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@push_bp.route('/enregistrerToken', methods=['POST'])
def enregistrer_token():
    """
    Endpoint pour enregistrer ou mettre à jour un token FCM pour un utilisateur.
    """
    try:
        data = request.json

        utilisateur_id = data.get('utilisateurId')
        fcm_token = data.get('fcmToken')

        if not utilisateur_id or not fcm_token:
            return jsonify({"error": "Données manquantes : utilisateurId et fcmToken sont requis."}), 400

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
