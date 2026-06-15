from sqlalchemy import select
from model.configuration import Configuration


def get_all(session):
    return session.execute(select(Configuration)).scalars().all()

def get_by_id(session, configuration_id):
    return session.get(Configuration, configuration_id)

def get_by_client(session, client_id):
    return session.execute(select(Configuration).filter_by(client_id=client_id)).scalars().all()

def save(session, configuration):
    session.add(configuration)
    session.commit()
    return configuration

def delete(session, configuration):
    session.delete(configuration)
    session.commit()
