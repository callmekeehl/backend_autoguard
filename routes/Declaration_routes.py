from flask import Blueprint, request, jsonify
from models import Declaration, Notification, Rdv, Police, Garage
from models.Utilisateur import Utilisateur
from app import db

declaration_bp = Blueprint('declaration_bp', __name__)

# routes.py (ajoutez ce code à la suite de celui existant)
from models.Declaration import Declaration

@declaration_bp.route('/declarations', methods=['GET', 'POST'])
def handle_declarations():
    if request.method == 'POST':
        data = request.get_json()
        new_declaration = Declaration(
            utilisateurId=data['utilisateurId'],
            nomProprio=data['nomProprio'],
            prenomProprio=data['prenomProprio'],
            telephoneProprio=data['telephoneProprio'],
            lieuLong=data['lieuLong'],
            lieuLat=data['lieuLat'],
            photoCarteGrise=data['photoCarteGrise'],
            numChassis=data['numChassis'],
            numPlaque=data['numPlaque'],
            marque=data['marque'],
            modele=data['modele'],
            dateHeure=data['dateHeure'],
            statut=data['statut']
        )
        db.session.add(new_declaration)
        db.session.commit()
        return jsonify({"message": "Déclaration créée"}), 201

    if request.method == 'GET':
        declarations = Declaration.query.all()
        return jsonify([d.to_dict() for d in declarations])

@declaration_bp.route('/declarations/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_declaration(id):
    declaration = Declaration.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(declaration.to_dict())

    if request.method == 'PUT':
        data = request.get_json()
        declaration.utilisateurId = data['utilisateurId']
        declaration.nomProprio = data['nomProprio']
        declaration.prenomProprio = data['prenomProprio']
        declaration.telephoneProprio = data['telephoneProprio']
        declaration.lieuLong = data['lieuLong']
        declaration.lieuLat = data['lieuLat']
        declaration.photoCarteGrise = data['photoCarteGrise']
        declaration.numChassis = data['numChassis']
        declaration.numPlaque = data['numPlaque']
        declaration.marque = data['marque']
        declaration.modele = data['modele']
        declaration.dateHeure = data['dateHeure']
        declaration.statut = data['statut']
        db.session.commit()
        return jsonify({"message": "Déclaration mise à jour"})

    if request.method == 'DELETE':
        db.session.delete(declaration)
        db.session.commit()
        return jsonify({"message": "Déclaration supprimée"})