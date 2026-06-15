from flask import Blueprint, g, jsonify, request
from controller.auth_controller import token_required, role_required
from persistence.db_config import get_session
from service import configuration_service

configuration_bp = Blueprint("configuration", __name__, url_prefix="/api/configurations")


@configuration_bp.route("/", methods=["GET"])
@token_required
@role_required("client", "admin")
def get_all():
    session = get_session()
    try:
        if g.user_ruolo == "admin":
            configs = configuration_service.get_all(session)
        else:
            configs = configuration_service.get_by_client(session, g.user_id)
        return jsonify([c.to_dict_full() for c in configs])
    finally:
        session.close()


@configuration_bp.route("/<int:configuration_id>", methods=["GET"])
@token_required
@role_required("client", "admin")
def get_by_id(configuration_id):
    session = get_session()
    try:
        conf = configuration_service.get_by_id(session, configuration_id)
        if g.user_ruolo == "client" and conf.client_id != g.user_id:
            return jsonify({"error": "Accesso negato!"}), 403
        return jsonify(conf.to_dict_full())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    finally:
        session.close()


@configuration_bp.route("/", methods=["POST"])
@token_required
@role_required("client")
def create():
    session = get_session()
    try:
        conf = configuration_service.create(session, request.get_json(), g.user_id)
        return jsonify(conf.to_dict_full()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@configuration_bp.route("/<int:configuration_id>", methods=["PUT"])
@token_required
@role_required("client", "admin")
def update(configuration_id):
    session = get_session()
    try:
        conf = configuration_service.update(
            session, configuration_id, request.get_json(),
            g.user_id, is_admin=(g.user_ruolo == "admin"),
        )
        return jsonify(conf.to_dict_full())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@configuration_bp.route("/<int:configuration_id>", methods=["DELETE"])
@token_required
@role_required("client", "admin")
def delete(configuration_id):
    session = get_session()
    try:
        configuration_service.delete(
            session, configuration_id, g.user_id, is_admin=(g.user_ruolo == "admin")
        )
        return jsonify({"message": f"Configurazione {configuration_id} eliminata!"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()
