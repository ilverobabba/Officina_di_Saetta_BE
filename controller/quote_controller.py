from flask import Blueprint, g, jsonify, request
from controller.auth_controller import token_required, role_required
from persistence.db_config import get_session
from service import quote_service

quote_bp = Blueprint("quote", __name__, url_prefix="/api/quotes")


@quote_bp.route("/", methods=["GET"])
@token_required
@role_required("client", "admin")
def get_all():
    session = get_session()
    try:
        if g.user_ruolo == "admin":
            quotes = quote_service.get_all(session)
        else:
            quotes = quote_service.get_by_client(session, g.user_id)
        return jsonify([q.to_dict() for q in quotes])
    finally:
        session.close()


@quote_bp.route("/<int:quote_id>", methods=["GET"])
@token_required
@role_required("client", "admin")
def get_by_id(quote_id):
    session = get_session()
    try:
        quote = quote_service.get_by_id(session, quote_id)
        if g.user_ruolo == "client" and quote.configuration.client_id != g.user_id:
            return jsonify({"error": "Accesso negato!"}), 403
        return jsonify(quote.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    finally:
        session.close()


@quote_bp.route("/generate/<int:configuration_id>", methods=["POST"])
@token_required
@role_required("client", "admin")
def genera(configuration_id):
    session = get_session()
    try:
        quote = quote_service.genera_preventivo(
            session, configuration_id, g.user_id,
            request.get_json() or {}, is_admin=(g.user_ruolo == "admin"),
        )
        return jsonify(quote.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@quote_bp.route("/<int:quote_id>/status", methods=["PUT"])
@token_required
@role_required("client", "admin")
def update_status(quote_id):
    session = get_session()
    try:
        data = request.get_json()
        if g.user_ruolo == "client":
            quote = quote_service.get_by_id(session, quote_id)
            if quote.configuration.client_id != g.user_id:
                return jsonify({"error": "Accesso negato!"}), 403
            if data.get("status") not in ["accepted", "rejected"]:
                return jsonify({"error": "Un client può solo accettare o rifiutare un preventivo!"}), 403
        quote = quote_service.update_status(session, quote_id, data, is_admin=(g.user_ruolo == "admin"))
        return jsonify(quote.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@quote_bp.route("/<int:quote_id>", methods=["DELETE"])
@token_required
@role_required("admin")
def delete(quote_id):
    session = get_session()
    try:
        quote_service.delete(session, quote_id, is_admin=True)
        return jsonify({"message": f"Preventivo {quote_id} eliminato!"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()
