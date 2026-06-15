from model.car_model import CarModel
from repository import car_model_repository, engine_repository, optional_repository


def get_all(session):
    return car_model_repository.get_all(session)


def get_by_id(session, model_id):
    model = car_model_repository.get_by_id(session, model_id)
    if not model:
        raise ValueError(f"Modello con id={model_id} non trovato!")
    return model


def create(session, data):
    if not all(k in data for k in ["name", "brand", "base_price", "engine_id"]):
        raise ValueError("Campi obbligatori: name, brand, base_price, engine_id")
    if float(data["base_price"]) < 0:
        raise ValueError("Il prezzo base non può essere negativo!")
    if not engine_repository.get_by_id(session, int(data["engine_id"])):
        raise ValueError(f"Engine con id={data['engine_id']} non trovato!")

    return car_model_repository.save(session, CarModel(
        name=data["name"],
        brand=data["brand"],
        base_price=float(data["base_price"]),
        category=data.get("category"),
        engine_id=int(data["engine_id"]),
    ))


def update(session, model_id, data):
    model = get_by_id(session, model_id)
    if "name" in data: model.name = data["name"]
    if "brand" in data: model.brand = data["brand"]
    if "category" in data: model.category = data["category"]
    if "base_price" in data:
        if float(data["base_price"]) < 0:
            raise ValueError("Il prezzo base non può essere negativo!")
        model.base_price = float(data["base_price"])
    if "engine_id" in data:
        if not engine_repository.get_by_id(session, int(data["engine_id"])):
            raise ValueError(f"Engine con id={data['engine_id']} non trovato!")
        model.engine_id = int(data["engine_id"])
    return car_model_repository.save(session, model)


def delete(session, model_id):
    car_model_repository.delete(session, get_by_id(session, model_id))


def add_optional(session, model_id, optional_id):
    model = get_by_id(session, model_id)
    opt = optional_repository.get_by_id(session, optional_id)
    if not opt:
        raise ValueError(f"Optional con id={optional_id} non trovato!")
    if opt in model.optionals:
        raise ValueError("Optional già associato a questo modello!")
    model.optionals.append(opt)
    session.commit()
    return model


def remove_optional(session, model_id, optional_id):
    model = get_by_id(session, model_id)
    opt = optional_repository.get_by_id(session, optional_id)
    if not opt:
        raise ValueError(f"Optional con id={optional_id} non trovato!")
    if opt not in model.optionals:
        raise ValueError("Optional non associato a questo modello!")
    model.optionals.remove(opt)
    session.commit()
    return model
