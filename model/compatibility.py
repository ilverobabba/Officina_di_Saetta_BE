from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from persistence.db_config import Base


class CompatibilityRule(Base):
    __tablename__ = "compatibility_rule"

    rule_id = Column(Integer, primary_key=True, autoincrement=True)
    rule_type = Column(String(50), nullable=False)  # "incompatible" | "requires"

    compatibilities = relationship("Compatibility", back_populates="rule", cascade="all, delete-orphan")

    def to_dict(self):
        return {"rule_id": self.rule_id, "rule_type": self.rule_type}


class Compatibility(Base):
    __tablename__ = "compatibility"

    compatibility_id = Column(Integer, primary_key=True, autoincrement=True)
    optional_id = Column(Integer, ForeignKey("optional.optional_id"), nullable=False)
    optional_with_id = Column(Integer, ForeignKey("optional.optional_id"), nullable=False)
    rule_id = Column(Integer, ForeignKey("compatibility_rule.rule_id"), nullable=False)

    optional = relationship("Optional", foreign_keys=[optional_id])
    optional_with = relationship("Optional", foreign_keys=[optional_with_id])
    rule = relationship("CompatibilityRule", back_populates="compatibilities")

    def to_dict(self):
        return {
            "compatibility_id": self.compatibility_id,
            "optional_id": self.optional_id,
            "optional_with_id": self.optional_with_id,
            "rule_id": self.rule_id,
            "rule_type": self.rule.rule_type if self.rule else None,
        }
