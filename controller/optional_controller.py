from flask import Blueprint, jsonify, request
from controller.auth_controller import token_required, role_required
from persistence.db_config import get_session
from service import optional_service

optional_bp = Blueprint("optional", __name__, url_prefix="/api/optionals")


@optional_bp.route("/", methods=["GET"])
def get_all():
    session = get_session()
    try:
        return jsonify([o.to_dict() for o in optional_service.get_all(session)])
    finally:
        session.close()


@optional_bp.route("/<int:optional_id>", methods=["GET"])
def get_by_id(optional_id):
    session = get_session()
    try:
        return jsonify(optional_service.get_by_id(session, optional_id).to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    finally:
        session.close()


@optional_bp.route("/", methods=["POST"])
@token_required
@role_required("admin")
def create():
    session = get_session()
    try:
        return jsonify(optional_service.create(session, request.get_json()).to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@optional_bp.route("/<int:optional_id>", methods=["PUT"])
@token_required
@role_required("admin")
def update(optional_id):
    session = get_session()
    try:
        return jsonify(optional_service.update(session, optional_id, request.get_json()).to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@optional_bp.route("/<int:optional_id>", methods=["DELETE"])
@token_required
@role_required("admin")
def delete(optional_id):
    session = get_session()
    try:
        optional_service.delete(session, optional_id)
        return jsonify({"message": f"Optional {optional_id} eliminato!"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    finally:
        session.close()
