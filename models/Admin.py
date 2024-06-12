
from app import db
from models.Utilisateur import Utilisateur


class Admin(Utilisateur):
    __tablename__ = 'admin'
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }
    adminId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utilisateurId = db.Column(db.Integer, db.ForeignKey('utilisateur.utilisateurId'), nullable=False, unique=True)
    utilisateur = db.relationship("Utilisateur", backref="admin", uselist=False)