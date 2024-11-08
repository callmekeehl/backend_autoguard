# models/vehicule_retrouve.py
from app import db
from datetime import datetime

class VehiculeRetrouve(db.Model):
    __tablename__ = 'vehicule_retrouve'
    
    vehicule_retrouve_id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, nullable=False)  # ID de l'utilisateur connecté
    nom_retrouveur = db.Column(db.String(100), nullable=False)
    prenom_retrouveur = db.Column(db.String(100), nullable=False)
    num_plaque = db.Column(db.String(20), nullable=False)
    lieu_long = db.Column(db.String(100), nullable=False)
    lieu_lat = db.Column(db.String(100), nullable=False)
    marque = db.Column(db.String(100), nullable=False)
    modele = db.Column(db.String(100), nullable=False)
    date_heure = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "vehicule_retrouve_id": self.vehicule_retrouve_id,
            "utilisateur_id": self.utilisateur_id,
            "nom_retrouveur": self.nom_retrouveur,
            "prenom_retrouveur": self.prenom_retrouveur,
            "num_plaque": self.num_plaque,
            "lieu_long": self.lieu_long,
            "lieu_lat": self.lieu_lat,
            "marque": self.marque,
            "modele": self.modele,
            "date_heure": self.date_heure,
        }
