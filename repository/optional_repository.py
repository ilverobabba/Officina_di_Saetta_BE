from sqlalchemy import select
from model.optional import Optional
from model.car_model import model_optional


def get_all(session):
    return session.execute(select(Optional)).scalars().all()

def get_by_id(session, optional_id):
    return session.get(Optional, optional_id)

def get_by_model(session, model_id):
    return session.execute(
        select(Optional).join(model_optional).where(model_optional.c.model_id == model_id)
    ).scalars().all()

def save(session, optional):
    session.add(optional)
    session.commit()
    return optional

def delete(session, optional):
    session.delete(optional)
    session.commit()
