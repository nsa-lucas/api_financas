from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from app.extensions import blacklist
from app.services.auth_services import auth, protected

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/signin", methods=["POST"])
def login():
    data = request.json

    response, status = auth(data)

    return jsonify(response), status


@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected_route():

    response, status = protected()

    return jsonify(response), status


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)

    return jsonify({"message": "Exiting..."})
