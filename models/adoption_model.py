"""认养记录模型."""

from sqlalchemy import Column, String, Float, Integer, DateTime
from database import Base
from datetime import datetime


class Adoption(Base):
    __tablename__ = "adoption"

    id = Column(Integer, primary_key=True, autoincrement=True)
    adoption_id = Column(String(64), unique=True, nullable=False)
    sheep_id = Column(String(64), nullable=False)
    adopter_name = Column(String(32), default="")
    adopter_phone = Column(String(16), default="")
    adopter_address = Column(String(128), default="")
    price = Column(Float, default=0.0)
    duration_months = Column(Integer, default=12)
    status = Column(String(16), default="pending")  # pending / active / completed / cancelled
    created_at = Column(DateTime, default=datetime.now)
