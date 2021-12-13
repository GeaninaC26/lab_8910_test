from Domain.entity import Entity
from Domain.undo_redo_operations import UndoRedoOperation
from Repository.repository import Repository


class UpdateOperation(UndoRedoOperation):

    def __init__(self,
                 repository: Repository,
                 updated_entity: Entity,
                 original_entity: Entity):
        self.repository = repository
        self.updated_entity = updated_entity
        self.original_entity = original_entity

    def undo(self):
        self.repository.update(self.original_entity)

    def redo(self):
        self.repository.update(self.updated_entity)
