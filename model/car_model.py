from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Table
from sqlalchemy.orm import relationship
from persistence.db_config import Base

model_optional = Table(
    "model_optional", Base.metadata,
    Column("model_id", Integer, ForeignKey("model.model_id"), primary_key=True),
    Column("optional_id", Integer, ForeignKey("optional.optional_id"), primary_key=True),
)


class CarModel(Base):
    __tablename__ = "model"

    model_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    brand = Column(String(100), nullable=False)
    base_price = Column(Numeric(10, 2), nullable=False)
    category = Column(String(50))
    engine_id = Column(Integer, ForeignKey("engine.engine_id"), nullable=False)

    engine = relationship("Engine")
    optionals = relationship("Optional", secondary="model_optional", back_populates="car_models")
    configurations = relationship("Configuration", back_populates="car_model")

    def to_dict(self):
        return {
            "model_id": self.model_id,
            "name": self.name,
            "brand": self.brand,
            "base_price": float(self.base_price),
            "category": self.category,
            "engine": self.engine.to_dict() if self.engine else None,
        }

    def to_dict_full(self):
        d = self.to_dict()
        d["optionals"] = [o.to_dict() for o in self.optionals]
        return d
