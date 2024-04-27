# -*- coding: utf-8 -*-
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, unique=False)

    calculations = relationship("Calculation", back_populates="owner")


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(DateTime, server_default=func.now())
    base_currency = Column(String(5))
    total = Column(Numeric(precision=16, scale=6))

    owner_id = Column(BigInteger, ForeignKey("users.id"))
    owner = relationship("User", back_populates="calculations")

    assets = relationship("Asset", back_populates="calculation")


class Asset(Base):
    __tablename__ = "assets"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    currency = Column(String(5))
    sum = Column(Numeric(precision=15, scale=6))

    calc_id = Column(Integer, ForeignKey("calculations.id"))
    calculation = relationship("Calculation", back_populates="assets")
