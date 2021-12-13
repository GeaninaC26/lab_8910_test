import datetime
from datetime import date
from typing import List

from Domain.add_operation import AddOperation
from Domain.delete_list_operation import DeleteListOperation
from Domain.delete_operation import DeleteOperation
from Domain.transaction import Transaction
from Domain.update_operation import UpdateOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService
from utils import my_sorted


class TransactionService:
    def __init__(self,
                 transaction_repository: Repository,
                 car_repository: Repository,
                 client_card_repository: Repository,
                 undo_redo_service: UndoRedoService):
        self.transaction_repository = transaction_repository
        self.car_repository = car_repository
        self.client_card_repository = client_card_repository
        self.undo_redo_service = undo_redo_service

    def add_transaction(self,
                        id_transaction: str,
                        id_car: str,
                        id_client_card: str,
                        parts_price: float,
                        workmanship_price: float,
                        date_time: str
                        ):
        """
        TODO
        """
        car = self.car_repository.read(id_car)
        if id_client_card is not None:
            self.client_card_repository.read(id_client_card)
            workmanship_price = \
                float(workmanship_price) - 10 * \
                float(workmanship_price) / 100
        if car.assurance == 'yes':
            parts_price = 0
        transaction = \
            Transaction(id_transaction, id_car, id_client_card,
                        parts_price, workmanship_price,
                                  date_time)
        self.transaction_repository.create(transaction)

        self.undo_redo_service.clear_redo()
        add_operation = \
            AddOperation(self.transaction_repository, transaction)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_transaction(self,
                           id_transaction: str,
                           id_car: str,
                           id_client_card: str,
                           parts_price: float,
                           workmanship_price: float,
                           date_time: str):
        """
        TODO
        """
        transaction2 = \
            self.transaction_repository.read(id_transaction)
        transaction = Transaction(id_transaction, id_car,
                                  id_client_card, parts_price,
                                  workmanship_price, date_time)
        self.transaction_repository.update(transaction)

        self.undo_redo_service.clear_redo()
        update_operation = \
            UpdateOperation(self.transaction_repository,
                            transaction, transaction2)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_transaction(self, id_transaction: str):
        transaction = \
            self.transaction_repository.read(id_transaction)
        self.transaction_repository.delete(id_transaction)

        self.undo_redo_service.clear_redo()
        delete_operation = \
            DeleteOperation(self.transaction_repository, transaction)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_all(self) -> List[Transaction]:
        return self.transaction_repository.read()

    def transaction_in_interval(self, a, b):
        return list(filter(lambda transaction:
                           a <=
                           int(transaction.workmanship_price +
                               transaction.parts_price)
                           <= b,
                           self.transaction_repository.read()))

    def descending_order_car(self):
        result = {transaction.id_car: 0 for transaction in
                  self.transaction_repository.read()}
        for i in self.transaction_repository.read():
            result[i.id_car] += int(i.workmanship_price)
        return list(map(
            lambda x: self.car_repository.read(x),
            my_sorted(list(result), key=lambda x: result[x],
                      reverse=True)))

    def descending_order_card(self):
        result = {transaction.id_client_card: 0 for transaction in
                  self.transaction_repository.read()}
        for i in self.transaction_repository.read():
            result[i.id_client_card] += int(i.workmanship_price)*0.9
        lst = list(result)
        return list(map(
            lambda x: self.client_card_repository.read(x),
            my_sorted(lst, key=lambda x: result[x], reverse=True)))

    def delete_between_days(self, first_day, last_day):
        low = list(map(int, first_day.split('/')))
        high = list(map(int, last_day.split('/')))
        first_day = date(low[2], low[1], low[0])
        last_day = date(high[2], high[1], high[0])
        deleted = []
        for i in self.transaction_repository.read():
            data = list(i.date_time.split('/'))
            data1 = list(data[2].split(' '))
            datai = date(int(data1[0]), int(data[1]), int(data[0]))
            if first_day <= datai <= last_day:
                deleted.append(i)
                self.transaction_repository.delete(i.id_entity)

        self.undo_redo_service.clear_redo()
        deleted_operation = \
            DeleteListOperation(self.transaction_repository, deleted)
        self.undo_redo_service.add_to_undo(deleted_operation)
