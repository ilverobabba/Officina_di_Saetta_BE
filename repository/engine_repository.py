from sqlalchemy import select
from model.engine import Engine


def get_all(session):
    return session.execute(select(Engine)).scalars().all()

def get_by_id(session, engine_id):
    return session.get(Engine, engine_id)

def save(session, engine):
    session.add(engine)
    session.commit()
    return engine

def delete(session, engine):
    session.delete(engine)
    session.commit()
