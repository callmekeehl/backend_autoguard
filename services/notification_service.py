from firebase_admin import messaging, credentials, initialize_app
import json

# Initialiser Firebase Admin SDK avec la clé JSON
cred = credentials.Certificate("config/serviceAccountKey.json")  # Remplace par le chemin de la clé JSON
initialize_app(cred)

def envoyer_notification_push(utilisateur_token, titre, message):
    """
    Envoie une notification push à un utilisateur spécifique via FCM.
    
    :param utilisateur_token: Le token FCM de l'utilisateur cible.
    :param titre: Titre de la notification.
    :param message: Corps de la notification.
    """
    try:
        # Créer le message de notification
        notification = messaging.Message(
            notification=messaging.Notification(
                title=titre,
                body=message
            ),
            token=utilisateur_token
        )

        # Envoyer la notification
        response = messaging.send(notification)
        return {"success": True, "response": response}
    
    except Exception as e:
        return {"success": False, "error": str(e)}
