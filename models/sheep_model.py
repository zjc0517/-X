"""羊只数据模型."""

from sqlalchemy import Column, String, Float, Integer, DateTime
from database import Base
from datetime import datetime


class Sheep(Base):
    __tablename__ = "sheep"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sheep_id = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(32), default="")
    breed = Column(String(32), default="")
    ranch_id = Column(String(64), default="")
    birth_date = Column(String(16), default="")
    gender = Column(String(8), default="female")
    weight_kg = Column(Float, default=0.0)
    price = Column(Float, default=0.0)
    status = Column(String(16), default="available")  # available / adopted / delivered
    adopter_id = Column(String(64), default="")
    image_url = Column(String(256), default="")
    created_at = Column(DateTime, default=datetime.now)
