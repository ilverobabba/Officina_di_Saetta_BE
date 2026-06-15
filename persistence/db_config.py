from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

engine = create_engine("postgresql://postgres:postgres@localhost/configuratore_auto", echo=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    # Import necessari per registrare i modelli prima di create_all
    import model.user
    import model.engine
    import model.car_model
    import model.optional
    import model.compatibility
    import model.configuration
    import model.quote

    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()
