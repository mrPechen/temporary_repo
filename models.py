from dataclasses import dataclass
from typing import Optional


@dataclass
class Vehicle:
    name: str
    model: str
    year: int
    color: str
    price: int
    latitude: float
    longitude: float
    id: Optional[int] = None
    