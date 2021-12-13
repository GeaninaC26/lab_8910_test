import random
import string
from datetime import date
from typing import List

from Domain.add_operation import AddOperation
from Domain.car_validator import CarValidator
from Domain.car import Car
from Domain.car_validator import CarValidator
from Domain.delete_list_operation import DeleteListOperation
from Domain.delete_operation import DeleteOperation
from Domain.generate_operation import GenerateListOperation
from Domain.update_list_operation import UpdateListOperation
from Domain.update_operation import UpdateOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class CarService:
    def __init__(self,
                 car_repository: Repository,
                 car_validator: CarValidator,
                 transaction_repository: Repository,
                 undo_redo_service: UndoRedoService):
        self.car_validator = car_validator
        self.car_repository = car_repository
        self.undo_redo_service = undo_redo_service
        self.transaction_repository = transaction_repository

    def add_car(self,
                id_car: str,
                model: str,
                purchase_year: int,
                km_number: float,
                assurance: bool):
        """
        TODO
        """
        car = Car(id_car, model, purchase_year,
                  km_number, assurance)
        self.car_validator.validate_car(car)
        self.car_repository.create(car)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.car_repository, car)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_car(self,
                   id_car: str,
                   model: str,
                   purchase_year: int,
                   km_number: float,
                   assurance: bool):
        """
        TODO
        """
        car2 = self.car_repository.read(id_car)
        car = Car(id_car, model, purchase_year,
                  km_number, assurance)
        self.car_validator.validate_car(car)
        self.car_repository.update(car)

        self.undo_redo_service.clear_redo()
        update_operation = \
            UpdateOperation(self.car_repository, car, car2)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_car(self, id_car: str):
        car = self.car_repository.read(id_car)
        self.car_repository.delete(id_car)
        deleted = []
        for i in self.transaction_repository.read():
            if i.id_car == id_car:
                deleted.append(i)
                self.transaction_repository.delete(i.id_entity)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.car_repository, car)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_all(self) -> List[Car]:
        return self.car_repository.read()

    def handle_search(self, search_params):
        # performs search_params on every field on all cars
        # returns: list of cars, in which search_params was found
        cars = self.car_repository.read()

        def search_rec(clist: list, search: str) -> List[Car]:
            res = []
            if len(clist) == 0:
                return []
            if search in clist[0].model or search_params \
                    in str(clist[0].purchase_year) or \
                    search_params in str(clist[0].km_number) or \
                    search_params in \
                    ('yes' if clist[0].assurance else 'no'):
                res.append(clist[0])
            res += (search_rec(clist[1:], search))
            return res

        result = search_rec(cars, search_params)
        return result

    def handle_generate_entity(self):
        created = []
        id_car = str(random.randint(1, 10000))
        model = ''.join(random.choices(string.ascii_lowercase,
                                       k=random.randint(4, 10)))
        purchase_year = random.randint(1950, date.today().year)
        km_number = random.randint(0, 1000000)
        assurance = 'yes' if random.randint(0, 1) == 1 else 'no'
        car = Car(id_car, model, purchase_year,
                  km_number, assurance)
        self.car_validator.validate_car(car)
        return car

    def handle_generate(self, n):
        generated = []
        for i in range(int(n)):
            car = self.handle_generate_entity()
            self.car_repository.create(car)
            generated.append(car)
        self.undo_redo_service.clear_redo()
        generate = GenerateListOperation(self.car_repository, generated)
        self.undo_redo_service.add_to_undo(generate)

    def update_assurance(self):
        initial = self.car_repository.read()
        updated = []
        for i in self.car_repository.read():
            if date.today().year - \
                    i.purchase_year > 3 or i.km_number > 60000:
                i.assurance = 'no'
            else:
                i.assurance = 'yes'
            self.car_repository.update(i)
            updated.append(i)

        self.undo_redo_service.clear_redo()
        updated_operation = \
            UpdateListOperation(self.car_repository, initial, updated)
        self.undo_redo_service.add_to_undo(updated_operation)
