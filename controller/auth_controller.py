from functools import wraps
from flask import Blueprint, g, jsonify, request
from persistence.db_config import get_session
from repository import user_repository
from service import auth_service

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")



def handle(fn, *args, status=200, **kwargs):
    """Esegue fn(session, ...) gestendo sessione ed errori in modo uniforme."""
    session = get_session()
    try:
        result = fn(session, *args, **kwargs)
        return jsonify(result), status
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        parts = header.split()
        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({"error": "Token mancante!"}), 401
        try:
            payload = auth_service.verifica_token(parts[1])
            g.user_id = payload["user_id"]
            g.user_email = payload["email"]
            g.user_ruolo = payload["ruolo"]
        except ValueError as e:
            return jsonify({"error": str(e)}), 401
        return f(*args, **kwargs)
    return decorated


def role_required(*ruoli_ammessi):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if g.user_ruolo not in ruoli_ammessi:
                return jsonify({"error": "Accesso negato! Ruolo non autorizzato."}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator



@auth_bp.route("/register", methods=["POST"])
def register():
    session = get_session()
    try:
        client = auth_service.register(session, request.get_json())
        return jsonify(client.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()


@auth_bp.route("/login", methods=["POST"])
def login():
    session = get_session()
    try:
        token, utente = auth_service.login(session, request.get_json())
        return jsonify({"token": token, "user": utente.to_dict()})
    except ValueError as e:
        return jsonify({"error": str(e)}), 401
    finally:
        session.close()


@auth_bp.route("/me")
@token_required
@role_required("client", "admin")
def me():
    session = get_session()
    try:
        return jsonify(user_repository.get_by_id(session, g.user_id).to_dict())
    finally:
        session.close()


@auth_bp.route("/users")
@token_required
@role_required("admin")
def get_all_users():
    session = get_session()
    try:
        return jsonify({
            "clients": [c.to_dict() for c in user_repository.get_all_clients(session)],
            "admins": [a.to_dict() for a in user_repository.get_all_admins(session)],
        })
    finally:
        session.close()


@auth_bp.route("/admin", methods=["POST"])
@token_required
@role_required("admin")
def create_admin():
    session = get_session()
    try:
        admin = auth_service.create_admin(session, request.get_json())
        return jsonify(admin.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()
