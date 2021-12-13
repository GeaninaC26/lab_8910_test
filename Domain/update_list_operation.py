from typing import List

from Domain.entity import Entity
from Domain.undo_redo_operations import UndoRedoOperation
from Repository.repository import Repository


class UpdateListOperation(UndoRedoOperation):

    def __init__(self,
                 car_repository: Repository,
                 original_list: List[Entity],
                 updated_list: List[Entity]):
        self.repository = car_repository
        self.updated_list = updated_list
        self.original_list = original_list

    def undo(self):
        for i in self.original_list:
            self.repository.update(i)

    def redo(self):
        for i in self.updated_list:
            self.repository.update(i)
