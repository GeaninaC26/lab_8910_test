import datetime
from typing import List

from Domain.add_operation import AddOperation
from Domain.client_card import ClientCard
from Domain.delete_operation import DeleteOperation
from Domain.update_operation import UpdateOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class ClientCardService:
    def __init__(self,
                 client_card_repository: Repository,
                 undo_redo_service: UndoRedoService):
        self.client_card_repository = client_card_repository
        self.undo_redo_service = undo_redo_service

    def add_card(self,
                 id_client_card: str,
                 last_name: str,
                 first_name: str,
                 cnp: str,
                 birthday: datetime.date,
                 registration_date: datetime.date):
        """
        TODO
        """
        if cnp in \
                [card.CNP for card in
                 self.client_card_repository.read()]:
            raise ValueError('cnp deja in lista.')
        if len(cnp) != 13:
            raise ValueError('lungimea cnp-ului incorecta')
        client_card = ClientCard(id_client_card, last_name,
                                 first_name, cnp, birthday,
                                 registration_date)
        self.client_card_repository.create(client_card)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.client_card_repository,
                                     client_card)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_card(self,
                    id_client_card: str,
                    last_name: str,
                    first_name: str,
                    cnp: str,
                    birthday: datetime.date,
                    registration_date: datetime.date):
        """
        TODO
        """
        client2 = self.client_card_repository.read(id_client_card)
        client = ClientCard(id_client_card,
                            last_name, first_name,
                            cnp, birthday, registration_date)
        self.client_card_repository.update(client)

        self.undo_redo_service.clear_redo()
        update_operation = \
            UpdateOperation(self.client_card_repository,
                            client, client2)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_card(self, id_client_card: str):
        card = self.client_card_repository.read(id_client_card)
        self.client_card_repository.delete(id_client_card)
        self.undo_redo_service.clear_redo()
        delete_operation = \
            DeleteOperation(self.client_card_repository, card)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_all(self) -> List[ClientCard]:
        return self.client_card_repository.read()

    def handle_search(self, search_params):

        cards = self.client_card_repository.read()
        results = []
        for i in cards:
            if search_params in i.first_name or\
                    search_params in i.last_name \
                    or search_params in i.CNP or \
                    search_params in str(i.birthday) or \
                    search_params in str(i.registration_date):
                results.append(i)
        return results
