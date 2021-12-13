from typing import List

from Domain.entity import Entity
from Domain.undo_redo_operations import UndoRedoOperation
from Repository.repository import Repository


class GenerateListOperation(UndoRedoOperation):

    def __init__(self,
                 repository: Repository,
                 generated_list: List[Entity]):
        self.repository = repository
        self.generated_list = generated_list

    def undo(self):
        for i in self.generated_list:
            self.repository.delete(i.id_entity)

    def redo(self):
        for i in self.generated_list:
            self.repository.create(i)
