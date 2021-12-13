from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class Car(Entity):
    model: str
    purchase_year: int
    km_number: float
    assurance: bool
