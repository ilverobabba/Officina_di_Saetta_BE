from sqlalchemy import select
from model.car_model import CarModel


def get_all(session):
    return session.execute(select(CarModel)).scalars().all()

def get_by_id(session, model_id):
    return session.get(CarModel, model_id)

def save(session, car_model):
    session.add(car_model)
    session.commit()
    return car_model

def delete(session, car_model):
    session.delete(car_model)
    session.commit()
