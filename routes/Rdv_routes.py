from flask import Blueprint, request, jsonify
from models import Declaration, Notification, Rdv, Police, Garage
from models.Utilisateur import Utilisateur
from app import db

rdv_bp = Blueprint('rdv_bp', __name__)

from models.Rdv import Rdv


@rdv_bp.route('/rdvs', methods=['POST'])
def handle_rdvs():
    if request.method == 'POST':
        data = request.get_json()
        new_rdv = Rdv(
            utilisateurId=data['utilisateurId'],
            policeId=data['policeId'],
            date=data['date'],
            motif=data['motif']
        )
        db.session.add(new_rdv)
        db.session.commit()
        return jsonify({"message": "Rdv créé"}), 201


@rdv_bp.route('/rdvs', methods=['GET'])
def get_rdvs():
    rdvs = Rdv.query.all()
    return jsonify([r.to_dict() for r in rdvs])


@rdv_bp.route('/rdvs/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_rdv(id):
    rdv = Rdv.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(rdv.to_dict())

    if request.method == 'PUT':
        data = request.get_json()
        rdv.utilisateurId = data['utilisateurId']
        rdv.policeId = data['policeId']
        rdv.date = data['date']
        rdv.motif = data['motif']
        db.session.commit()
        return jsonify({"message": "Rdv mis à jour"})

    if request.method == 'DELETE':
        db.session.delete(rdv)
        db.session.commit()
        return jsonify({"message": "Rdv supprimé"})