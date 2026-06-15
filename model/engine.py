from sqlalchemy import Column, Integer, String, Numeric
from persistence.db_config import Base


class Engine(Base):
    __tablename__ = "engine"

    engine_id = Column(Integer, primary_key=True, autoincrement=True)
    fuel_type = Column(String(50), nullable=False)
    power_hp = Column(Integer, nullable=False)
    extra_price = Column(Numeric(10, 2), nullable=False, default=0)

    def to_dict(self):
        return {
            "engine_id": self.engine_id,
            "fuel_type": self.fuel_type,
            "power_hp": self.power_hp,
            "extra_price": float(self.extra_price),
        }
