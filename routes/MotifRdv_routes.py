from flask import Blueprint, request, jsonify
from app import db
from models.MotifRdv import MotifRdv
from datetime import datetime

motif_bp = Blueprint('motif_bp', __name__)

@motif_bp.route('/motifs', methods=['POST'])
def create_motif():
    data = request.get_json()
    utilisateur_id = data.get('utilisateurId')
    motif_description = data.get('motifDescription')
    date = data.get('date')

    if not utilisateur_id or not motif_description:
        return jsonify({"error": "Missing data"}), 400
    try:
        date_obj = datetime.fromisoformat(date)
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    motif_rdv = MotifRdv(
        utilisateurId=utilisateur_id, 
        motifDescription=motif_description, 
        date=date_obj
    )
    db.session.add(motif_rdv)
    db.session.commit()

    return jsonify(motif_rdv.to_dict()), 201

@motif_bp.route('/motifs', methods=['GET'])
def get_motifs():
    motifs = MotifRdv.query.all()
    return jsonify([motif.to_dict() for motif in motifs])

@motif_bp.route('/motifs/<int:id>', methods=['DELETE'])
def delete_motif(id):
    motif = MotifRdv.query.get_or_404(id)

    db.session.delete(motif)
    db.session.commit()

    return jsonify({'message': 'Motif supprimé avec succès'}), 204