from model.configuration import Configuration
from repository import configuration_repository, car_model_repository, engine_repository, optional_repository, user_repository
from service import compatibility_service


def _calcola_prezzo(car_model, engine, optionals):
    totale = float(car_model.base_price) + float(engine.extra_price)
    totale += sum(float(o.price) for o in optionals)
    return round(totale, 2)


def _carica_optionals(session, optional_ids, car_model):
    optionals = []
    for opt_id in optional_ids:
        opt = optional_repository.get_by_id(session, opt_id)
        if not opt:
            raise ValueError(f"Optional con id={opt_id} non trovato!")
        if opt not in car_model.optionals:
            raise ValueError(f"Optional '{opt.name}' non disponibile per il modello '{car_model.name}'!")
        optionals.append(opt)
    return optionals


def get_all(session):
    return configuration_repository.get_all(session)


def get_by_id(session, configuration_id):
    conf = configuration_repository.get_by_id(session, configuration_id)
    if not conf:
        raise ValueError(f"Configurazione con id={configuration_id} non trovata!")
    return conf


def get_by_client(session, client_id):
    return configuration_repository.get_by_client(session, client_id)


def create(session, data, client_id):
    if not all(k in data for k in ["name", "model_id", "engine_id"]):
        raise ValueError("Campi obbligatori: name, model_id, engine_id")

    if not user_repository.get_client_by_id(session, client_id):
        raise ValueError("Client non trovato!")

    car_model = car_model_repository.get_by_id(session, int(data["model_id"]))
    if not car_model:
        raise ValueError(f"Modello con id={data['model_id']} non trovato!")

    engine = engine_repository.get_by_id(session, int(data["engine_id"]))
    if not engine:
        raise ValueError(f"Engine con id={data['engine_id']} non trovato!")

    optional_ids = [int(x) for x in data.get("optional_ids", [])]
    optionals = _carica_optionals(session, optional_ids, car_model)

    violazioni = compatibility_service.check_optional_list(session, optional_ids)
    if violazioni:
        raise ValueError("Errori di compatibilità: " + " | ".join(v["message"] for v in violazioni))

    conf = Configuration(
        name=data["name"],
        status="draft",
        total_price=_calcola_prezzo(car_model, engine, optionals),
        client_id=client_id,
        model_id=car_model.model_id,
        engine_id=engine.engine_id,
    )
    conf.optionals = optionals
    return configuration_repository.save(session, conf)


def update(session, configuration_id, data, client_id, is_admin=False):
    conf = get_by_id(session, configuration_id)

    if not is_admin and conf.client_id != client_id:
        raise ValueError("Non sei autorizzato a modificare questa configurazione!")
    if conf.status == "quoted":
        raise ValueError("Impossibile modificare una configurazione per cui esiste già un preventivo!")

    if "name" in data:
        conf.name = data["name"]
    if "engine_id" in data:
        engine = engine_repository.get_by_id(session, int(data["engine_id"]))
        if not engine:
            raise ValueError(f"Engine con id={data['engine_id']} non trovato!")
        conf.engine_id = engine.engine_id
    if "optional_ids" in data:
        optional_ids = [int(x) for x in data["optional_ids"]]
        optionals = _carica_optionals(session, optional_ids, conf.car_model)
        violazioni = compatibility_service.check_optional_list(session, optional_ids)
        if violazioni:
            raise ValueError("Errori di compatibilità: " + " | ".join(v["message"] for v in violazioni))
        conf.optionals = optionals

    conf.total_price = _calcola_prezzo(
        conf.car_model,
        engine_repository.get_by_id(session, conf.engine_id),
        conf.optionals,
    )
    return configuration_repository.save(session, conf)


def delete(session, configuration_id, client_id, is_admin=False):
    conf = get_by_id(session, configuration_id)
    if not is_admin and conf.client_id != client_id:
        raise ValueError("Non sei autorizzato a eliminare questa configurazione!")
    configuration_repository.delete(session, conf)
