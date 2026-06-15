from model.optional import Optional
from repository import optional_repository


def get_all(session):
    return optional_repository.get_all(session)


def get_by_id(session, optional_id):
    opt = optional_repository.get_by_id(session, optional_id)
    if not opt:
        raise ValueError(f"Optional con id={optional_id} non trovato!")
    return opt


def create(session, data):
    if not all(k in data for k in ["name", "price"]):
        raise ValueError("Campi obbligatori: name, price")
    if float(data["price"]) < 0:
        raise ValueError("Il prezzo non può essere negativo!")

    return optional_repository.save(session, Optional(
        name=data["name"],
        category=data.get("category"),
        price=float(data["price"]),
    ))


def update(session, optional_id, data):
    opt = get_by_id(session, optional_id)
    if "name" in data:
        opt.name = data["name"]
    if "category" in data:
        opt.category = data["category"]
    if "price" in data:
        if float(data["price"]) < 0:
            raise ValueError("Il prezzo non può essere negativo!")
        opt.price = float(data["price"])
    return optional_repository.save(session, opt)


def delete(session, optional_id):
    optional_repository.delete(session, get_by_id(session, optional_id))
