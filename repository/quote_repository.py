from sqlalchemy import select
from model.quote import Quote
from model.configuration import Configuration


def get_all(session):
    return session.execute(select(Quote)).scalars().all()

def get_by_id(session, quote_id):
    return session.get(Quote, quote_id)

def get_by_client(session, client_id):
    return session.execute(
        select(Quote).join(Configuration).filter(Configuration.client_id == client_id)
    ).scalars().all()

def get_last(session):
    return session.execute(select(Quote).order_by(Quote.quote_id.desc())).scalars().first()

def save(session, quote):
    session.add(quote)
    session.commit()
    return quote

def delete(session, quote):
    session.delete(quote)
    session.commit()
