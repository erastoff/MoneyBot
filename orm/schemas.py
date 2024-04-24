# -*- coding: utf-8 -*-
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str = "unnamed"


class Calculation(BaseModel):
    id: int = None
    date: datetime = None
    base_currency: str
    total: Decimal = None
    owner_id: int


class Asset(BaseModel):
    id: int = None
    currency: str
    sum: Decimal
    calc_id: int
