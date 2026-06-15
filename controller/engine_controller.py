from flask import Blueprint, jsonify, request
from controller.auth_controller import token_required, role_required
from persistence.db_config import get_session
from service import engine_service

engine_bp = Blueprint("engine", __name__, url_prefix="/api/engines")


def _session_wrap(fn, *args, status=200):
    session = get_session()
    try:
        return jsonify(fn(session, *args)), status
    except ValueError as e:
        return jsonify({"error": str(e)}), 400 if status != 200 else 404
    finally:
        session.close()


@engine_bp.route("/", methods=["GET"])
def get_all():
    session = get_session()
    try:
        return jsonify([e.to_dict() for e in engine_service.get_all(session)])
    finally:
        session.close()


@engine_bp.route("/<int:engine_id>", methods=["GET"])
def get_by_id(engine_id):
    session = get_session()
    try:
        return jsonify(engine_service.get_by_id(session, engine_id).to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    finally:
        session.close()


@engine_bp.route("/", methods=["POST"])
@token_required
@role_required("admin")
def create():
    session = get_session()
    try:
        return jsonify(engine_service.create(session, request.get_json()).to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@engine_bp.route("/<int:engine_id>", methods=["PUT"])
@token_required
@role_required("admin")
def update(engine_id):
    session = get_session()
    try:
        return jsonify(engine_service.update(session, engine_id, request.get_json()).to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@engine_bp.route("/<int:engine_id>", methods=["DELETE"])
@token_required
@role_required("admin")
def delete(engine_id):
    session = get_session()
    try:
        engine_service.delete(session, engine_id)
        return jsonify({"message": f"Engine {engine_id} eliminato!"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    finally:
        session.close()
