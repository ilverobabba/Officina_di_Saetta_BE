import datetime
import bcrypt
import jwt

from model.user import Client, Admin
from repository import user_repository

SECRET_KEY = "cambiami-in-produzione"


def _hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def register(session, data):
    if not all(data.get(c) for c in ["first_name", "last_name", "email", "password"]):
        raise ValueError("Campi obbligatori: first_name, last_name, email, password")

    if user_repository.get_by_email(session, data["email"]):
        raise ValueError("Email già registrata!")

    client = Client(
        email=data["email"],
        password_hash=_hash(data["password"]),
        first_name=data["first_name"],
        last_name=data["last_name"],
        phone=data.get("phone"),
    )
    return user_repository.save(session, client)


def create_admin(session, data):
    if not all(data.get(c) for c in ["email", "password"]):
        raise ValueError("Campi obbligatori: email, password")

    if user_repository.get_by_email(session, data["email"]):
        raise ValueError("Email già registrata!")

    admin = Admin(email=data["email"], password_hash=_hash(data["password"]))
    return user_repository.save(session, admin)


def login(session, data):
    if not data.get("email") or not data.get("password"):
        raise ValueError("Email e password obbligatori!")

    utente = user_repository.get_by_email(session, data["email"])
    if not utente or not bcrypt.checkpw(data["password"].encode(), utente.password_hash.encode()):
        raise ValueError("Credenziali non valide!")

    payload = {
        "user_id": utente.user_id,
        "email": utente.email,
        "ruolo": utente.tipo,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=8),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token, utente


def verifica_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token scaduto!")
    except jwt.InvalidTokenError:
        raise ValueError("Token non valido!")
