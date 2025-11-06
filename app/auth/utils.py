from flask import jsonify

from app.auth.extensions import jwt, blacklist
from app.models.user import User


@jwt.unauthorized_loader
def unauthorized_access(error):
    return jsonify({"message": "Authentication required"}), 401


@jwt.invalid_token_loader
def invalid_token(error):
    return jsonify({"message": "Invalid token"}), 401


@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return jsonify({"message": "Token has expired"}), 401


@jwt.revoked_token_loader
def revoked_token(jwt_header, jwt_payload):
    return jsonify({"message": "Token has been revoked"}), 401


@jwt.user_lookup_error_loader
def user_lookup_error_callback(jwt_header, jwt_data):
    return jsonify({"message": "User identity invalid"}), 401


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blacklist


@jwt.user_lookup_loader
def load_user(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.get(identity)
