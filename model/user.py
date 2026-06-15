from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from persistence.db_config import Base


class User(Base):
    __tablename__ = "app_user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(20), nullable=False)  # "client" | "admin"
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": tipo,
        "polymorphic_identity": "user",
    }

    def to_dict(self):
        return {"user_id": self.user_id, "tipo": self.tipo, "email": self.email}


class Client(User):
    __tablename__ = "client"

    client_id = Column(Integer, ForeignKey("app_user.user_id"), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(30))

    configurations = relationship("Configuration", back_populates="client", cascade="all, delete-orphan")

    __mapper_args__ = {"polymorphic_identity": "client"}

    def to_dict(self):
        d = super().to_dict()
        d.update({"first_name": self.first_name, "last_name": self.last_name, "phone": self.phone})
        return d


class Admin(User):
    __tablename__ = "admin"

    admin_id = Column(Integer, ForeignKey("app_user.user_id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "admin"}
