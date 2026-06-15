from flask import Blueprint, jsonify, request
from controller.auth_controller import token_required, role_required
from persistence.db_config import get_session
from service import compatibility_service

compatibility_bp = Blueprint("compatibility", __name__, url_prefix="/api/compatibility")


@compatibility_bp.route("/rules", methods=["GET"])
@token_required
@role_required("admin")
def get_all_rules():
    session = get_session()
    try:
        return jsonify([r.to_dict() for r in compatibility_service.get_all_rules(session)])
    finally:
        session.close()


@compatibility_bp.route("/rules", methods=["POST"])
@token_required
@role_required("admin")
def create_rule():
    session = get_session()
    try:
        return jsonify(compatibility_service.create_rule(session, request.get_json()).to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@compatibility_bp.route("/rules/<int:rule_id>", methods=["DELETE"])
@token_required
@role_required("admin")
def delete_rule(rule_id):
    session = get_session()
    try:
        compatibility_service.delete_rule(session, rule_id)
        return jsonify({"message": f"Regola {rule_id} eliminata!"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    finally:
        session.close()


@compatibility_bp.route("/", methods=["GET"])
@token_required
@role_required("admin")
def get_all():
    session = get_session()
    try:
        return jsonify([c.to_dict() for c in compatibility_service.get_all_compatibilities(session)])
    finally:
        session.close()


@compatibility_bp.route("/", methods=["POST"])
@token_required
@role_required("admin")
def create():
    session = get_session()
    try:
        return jsonify(compatibility_service.create_compatibility(session, request.get_json()).to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@compatibility_bp.route("/<int:compatibility_id>", methods=["DELETE"])
@token_required
@role_required("admin")
def delete(compatibility_id):
    session = get_session()
    try:
        compatibility_service.delete_compatibility(session, compatibility_id)
        return jsonify({"message": f"Compatibility {compatibility_id} eliminata!"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    finally:
        session.close()


@compatibility_bp.route("/check", methods=["POST"])
@token_required
@role_required("client", "admin")
def check():
    session = get_session()
    try:
        optional_ids = [int(x) for x in request.get_json().get("optional_ids", [])]
        violazioni = compatibility_service.check_optional_list(session, optional_ids)
        return jsonify({"valid": len(violazioni) == 0, "violations": violazioni})
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()
