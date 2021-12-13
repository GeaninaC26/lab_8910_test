from Domain.car_validator import CarValidator
from Repository.json_repository import JsonRepository
from Service.car_service import CarService
from Service.client_card_service import ClientCardService
from Service.transaction_service import TransactionService
from Service.undo_redo_service import UndoRedoService
from Test.test_repository import test_car_repo, test_all_repo
from Test.test_service import test_all_service
from Test.test_undo_redo import test_all
from UserInterface.console import Console


def main():
    car_repo = JsonRepository('car.json')
    card_repo = JsonRepository('card.json')
    transaction_repo = \
        JsonRepository('transaction.json')

    car_validator = CarValidator()

    undo_redo_service = UndoRedoService()

    car_service = CarService(car_repo,
                             car_validator,
                             transaction_repo,
                             undo_redo_service)
    card_service = ClientCardService(card_repo,
                                     undo_redo_service)
    transaction_service = TransactionService(transaction_repo,
                                             car_repo,
                                             card_repo,
                                             undo_redo_service)

    console = Console(car_service,
                      card_service,
                      transaction_service,
                      undo_redo_service)

    console.run_console()


if __name__ == '__main__':
    test_all_repo()
    test_all_service()
    test_all()
    main()
