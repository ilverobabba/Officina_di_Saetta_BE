from sqlalchemy import select
from model.user import User, Client, Admin


def get_by_email(session, email):
    return session.execute(select(User).filter_by(email=email)).scalars().first()

def get_by_id(session, user_id):
    return session.get(User, user_id)

def get_client_by_id(session, client_id):
    return session.get(Client, client_id)

def get_all_clients(session):
    return session.execute(select(Client)).scalars().all()

def get_all_admins(session):
    return session.execute(select(Admin)).scalars().all()

def save(session, user):
    session.add(user)
    session.commit()
    return user
