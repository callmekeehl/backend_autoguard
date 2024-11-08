from flask import Blueprint, jsonify
from models import Utilisateur, Police, Garage, Declaration, Rdv

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    # Récupérer le nombre total d'utilisateurs, polices, garages et déclarations
    utilisateurs_count = Utilisateur.query.count()
    polices_count = Police.query.count()
    garages_count = Garage.query.count()
    declarations_count = Declaration.query.count()
    rdv_count = Rdv.query.count()

    # Créer un dictionnaire avec les statistiques
    stats = {
        'utilisateurs': utilisateurs_count,
        'polices': polices_count,
        'garages': garages_count,
        'declarations': declarations_count,
        'rdvs': rdv_count
    }

    return jsonify(stats), 200
