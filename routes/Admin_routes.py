from flask import Blueprint, request, jsonify
from models.Admin import Admin
from models.Utilisateur import Utilisateur
from app import db

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/admins', methods=['POST'])
def create_admin():
    data = request.get_json()

    print("Données JSON reçues:", data)

    required_fields = ['nom', 'prenom', 'email', 'adresse', 'telephone', 'motDePasse']
    missing_fields = [field for field in required_fields if field not in data or not data[field]]

    if missing_fields:
        return jsonify({"error": f"Les champs suivants sont manquants ou vides: {', '.join(missing_fields)}"}), 400

    if Utilisateur.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Un utilisateur avec cet email existe déjà."}), 400

    try:
        # Créez l'utilisateur et assignez directement le type 'admin'
        new_user = Admin(
            nom=data['nom'],
            prenom=data['prenom'],
            email=data['email'],
            adresse=data['adresse'],
            telephone=data['telephone'],
            type='admin'  # Utilisez le polymorphic_identity 'admin'
        )
        new_user.motDePasse = data['motDePasse']
        db.session.add(new_user)
        db.session.commit()  # Commit ici pour persister les changements

        return jsonify({"message": "Admin créé", "adminId": new_user.adminId}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



@admin_bp.route('/admins', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    return jsonify([a.to_dict() for a in admins])

@admin_bp.route('/admins/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_admin(id):
    admin = Admin.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(admin.to_dict())

    if request.method == 'PUT':
        data = request.get_json()

        utilisateur = Utilisateur.query.get(admin.utilisateurId)
        utilisateur.nom = data.get('nom', utilisateur.nom)
        utilisateur.prenom = data.get('prenom', utilisateur.prenom)
        utilisateur.email = data.get('email', utilisateur.email)
        utilisateur.adresse = data.get('adresse', utilisateur.adresse)
        utilisateur.telephone = data.get('telephone', utilisateur.telephone)

        if 'motDePasse' in data:
            utilisateur.motDePasse = data['motDePasse']  # Utiliser le setter pour mettre à jour le mot de passe hashé

        db.session.commit()
        return jsonify({"message": "Admin mis à jour"})

    if request.method == 'DELETE':
        try:
            db.session.delete(admin)
            db.session.commit()

            utilisateur = Utilisateur.query.get(admin.utilisateurId)
            if utilisateur:
                db.session.delete(utilisateur)
                db.session.commit()

            return jsonify({"message": "Admin supprimé"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500