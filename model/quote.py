from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from persistence.db_config import Base


class Quote(Base):
    __tablename__ = "quote"

    quote_id = Column(Integer, primary_key=True, autoincrement=True)
    quote_number = Column(String(30), unique=True, nullable=False)
    issued_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), nullable=False, default="pending")  # "pending" | "accepted" | "rejected" | "expired"
    final_price = Column(Numeric(10, 2), nullable=False)
    discount_pct = Column(Numeric(5, 2), nullable=False, default=0)
    configuration_id = Column(Integer, ForeignKey("configuration.configuration_id"), nullable=False, unique=True)

    configuration = relationship("Configuration", back_populates="quote")

    def to_dict(self):
        return {
            "quote_id": self.quote_id,
            "quote_number": self.quote_number,
            "issued_at": self.issued_at.isoformat() if self.issued_at else None,
            "status": self.status,
            "final_price": float(self.final_price),
            "discount_pct": float(self.discount_pct),
            "configuration_id": self.configuration_id,
        }
