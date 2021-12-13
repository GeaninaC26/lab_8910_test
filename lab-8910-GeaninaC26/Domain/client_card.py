from dataclasses import dataclass
import datetime

from Domain.entity import Entity


@dataclass
class ClientCard(Entity):
    last_name: str
    first_name: str
    CNP: str
    birthday: datetime.date
    registration_date: datetime.date
