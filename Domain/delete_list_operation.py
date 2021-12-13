from typing import List

from Domain.entity import Entity
from Domain.undo_redo_operations import UndoRedoOperation
from Repository.repository import Repository


class DeleteListOperation(UndoRedoOperation):

    def __init__(self,
                 repository: Repository,
                 deleted_list: List[Entity]):
        self.repository = repository
        self.deleted_list = deleted_list

    def undo(self):
        for i in self.deleted_list:
            self.repository.create(i)

    def redo(self):
        for i in self.deleted_list:
            self.repository.delete(i.id_entity)
