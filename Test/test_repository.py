import os
import datetime

from Domain.car import Car
from Domain.client_card import ClientCard
from Domain.transaction import Transaction
from Repository.json_repository import JsonRepository
from utils import clear_file


def test_car_repo():
    filename = 'test_car_repo.json'
    car_repo = JsonRepository(filename)
    added = Car('1', 'Dacia', 2012, 700000, True)
    car_repo.create(added)
    assert car_repo.read(added.id_entity) == added

    updated = Car('1', 'Opel', 2012, 700000, True)
    car_repo.update(updated)
    assert car_repo.read(updated.id_entity) == updated

    added2 = Car('2', 'Mercedes', 2013, 600000, False)
    car_repo.create(added2)
    assert car_repo.read(added2.id_entity) == added2

    id_entity = added2.id_entity
    car_repo.delete(id_entity)
    assert car_repo.read(id_entity) is None


def test_card_repo():
    card_repo = JsonRepository('test_card_repo.json')
    added = ClientCard('1', 'Popa', 'Ioan',
                       '3050289040596', 5/2/1989, 20/5/2018)
    card_repo.create(added)
    assert card_repo.read(added.id_entity) == added

    updated = ClientCard('1', 'Popa', 'Ioan',
                         '30502890347596', 5/2/1989, 20/5/2018)
    card_repo.update(updated)
    assert card_repo.read(updated.id_entity) == updated

    added2 = ClientCard('2', 'Toma', 'Dan',
                        '1120702948375', 12/7/2002, 25/12/2020)
    card_repo.create(added2)
    assert card_repo.read(added2.id_entity) == added2

    id_entity = added2.id_entity
    card_repo.delete(id_entity)
    assert card_repo.read(id_entity) is None


def test_transaction_repo():
    transaction_repo = \
        JsonRepository('test_transaction_repo.json')
    date = \
        str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
    added = Transaction('1', '1', '1', 200, 500, date)
    transaction_repo.create(added)
    assert transaction_repo.read(added.id_entity) == added

    updated = Transaction('1', '2', '1', 300, 400, date)
    transaction_repo.update(updated)
    assert transaction_repo.read(added.id_entity) == updated

    added2 = Transaction('2', '1', '1', 500, 200, date)
    transaction_repo.create(added2)
    assert transaction_repo.read(added2.id_entity) == added2
    id_entity = added2.id_entity
    transaction_repo.delete(id_entity)
    assert transaction_repo.read(id_entity) is None


def test_all_repo():
    clear_file('test_car_repo.json')
    clear_file('test_card_repo.json')
    clear_file('test_transaction_repo.json')
    test_car_repo()
    test_card_repo()
    test_transaction_repo()
