import datetime

from model.quote import Quote
from repository import quote_repository, configuration_repository

STATI_VALIDI = ["pending", "accepted", "rejected", "expired"]


def _genera_numero(session):
    anno = datetime.datetime.now().year
    ultimo = quote_repository.get_last(session)
    try:
        progressivo = int(ultimo.quote_number.split("-")[-1]) + 1 if ultimo else 1
    except (ValueError, IndexError):
        progressivo = 1
    return f"QT-{anno}-{progressivo:04d}"


def get_all(session):
    return quote_repository.get_all(session)


def get_by_id(session, quote_id):
    quote = quote_repository.get_by_id(session, quote_id)
    if not quote:
        raise ValueError(f"Preventivo con id={quote_id} non trovato!")
    return quote


def get_by_client(session, client_id):
    return quote_repository.get_by_client(session, client_id)


def genera_preventivo(session, configuration_id, client_id, data=None, is_admin=False):
    data = data or {}
    conf = configuration_repository.get_by_id(session, configuration_id)
    if not conf:
        raise ValueError(f"Configurazione con id={configuration_id} non trovata!")
    if not is_admin and conf.client_id != client_id:
        raise ValueError("Non sei autorizzato a generare un preventivo per questa configurazione!")
    if conf.status == "quoted":
        raise ValueError("Esiste già un preventivo per questa configurazione!")

    discount_pct = float(data.get("discount_pct", 0))
    if not (0 <= discount_pct <= 100):
        raise ValueError("Lo sconto deve essere compreso tra 0 e 100!")

    final_price = round(float(conf.total_price) * (1 - discount_pct / 100), 2)
    conf.status = "quoted"
    session.commit()

    return quote_repository.save(session, Quote(
        quote_number=_genera_numero(session),
        status="pending",
        final_price=final_price,
        discount_pct=discount_pct,
        configuration_id=configuration_id,
    ))


def update_status(session, quote_id, data, is_admin=False):
    if data.get("status") not in STATI_VALIDI:
        raise ValueError(f"Status deve essere uno di: {STATI_VALIDI}")
    quote = get_by_id(session, quote_id)
    quote.status = data["status"]
    return quote_repository.save(session, quote)


def delete(session, quote_id, is_admin=False):
    if not is_admin:
        raise ValueError("Solo un admin può eliminare un preventivo!")
    quote = get_by_id(session, quote_id)
    if quote.configuration:
        quote.configuration.status = "saved"
        session.commit()
    quote_repository.delete(session, quote)
