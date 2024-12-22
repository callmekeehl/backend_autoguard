from app import db
from datetime import datetime

class NotificationLog(db.Model):
    __tablename__ = 'notification_logs'

    id = db.Column(db.Integer, primary_key=True)
    expediteur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    destinataire_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    titre = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_envoi = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    statut = db.Column(db.String(50), nullable=False)  # 'success' ou 'error'
    reponse_fcm = db.Column(db.Text)  # Réponse du serveur FCM

    expediteur = db.relationship('Utilisateur', foreign_keys=[expediteur_id])
    destinataire = db.relationship('Utilisateur', foreign_keys=[destinataire_id])

class FcmToken(db.Model):
    __tablename__ = 'fcm_tokens'

    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), unique=True, nullable=False)
    fcm_token = db.Column(db.String(255), nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_mise_a_jour = db.Column(db.DateTime, nullable=True)

    utilisateur = db.relationship('Utilisateur', backref=db.backref('fcm_token', uselist=False))