from datetime import datetime
from app import db
from models import Utilisateur


class Notification(db.Model):
    notificationId = db.Column(db.Integer, primary_key=True)
    utilisateurId = db.Column(db.Integer, db.ForeignKey('utilisateur.utilisateurId'), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    dateEnvoi = db.Column(db.DateTime, default=datetime.utcnow)
    lu = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "notificationId": self.notificationId,
            "utilisateurId": self.utilisateurId,
            "message": self.message,
            "dateEnvoi": self.dateEnvoi,
            "lu": self.lu,
        }