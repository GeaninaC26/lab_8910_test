from dataclasses import dataclass
from Domain.entity import Entity


@dataclass
class Transaction(Entity):
    id_car: str
    id_client_card: str
    parts_price: float
    workmanship_price: float
    date_time: str
