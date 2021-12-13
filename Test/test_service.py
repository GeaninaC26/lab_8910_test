from Domain.car import Car
from Domain.car_validator import CarValidator
from Domain.client_card import ClientCard
from Domain.transaction import Transaction
from Repository.json_repository import JsonRepository
from Service.car_service import CarService
from Service.client_card_service import ClientCardService
from Service.transaction_service import TransactionService
import datetime


from Service.undo_redo_service import UndoRedoService
from utils import clear_file


def test_car_service():
    car_repo = \
        JsonRepository('test_car_service.json')
    transaction_repo = \
        JsonRepository('test_transaction_service.json')
    car_validator = CarValidator()
    undo_redo_service = UndoRedoService()
    car_service = CarService(car_repo, car_validator,
                             transaction_repo,
                             undo_redo_service)
    # test add

    car_service.add_car('1', 'Dacia', 2012, 700000, 'yes')
    assert car_service.get_all() == \
           [Car(id_entity='1',
                model='Dacia',
                purchase_year=2012,
                km_number=700000,
                assurance='yes')]

    car_service.update_car('1', 'Skoda', 2015, 700000, 'yes')
    assert car_service.get_all() == \
           [Car(id_entity='1',
                model='Skoda',
                purchase_year=2015,
                km_number=700000,
                assurance='yes')]

    car_service.delete_car('1')
    assert car_service.get_all() == []
    car_service.add_car('1', 'Dacia', 2012, 700000, 'yes')
    car_service.handle_generate(2)
    assert len(car_service.get_all()) == 3
    car_service.update_assurance()
    assert car_repo.read('1').assurance == 'no'
    assert car_service.handle_search('Dacia') == \
           [Car(id_entity='1',
                model='Dacia',
                purchase_year=2012,
                km_number=700000,
                assurance='no')]
    car_service.add_car('2', 'Skoda', 2017, 600000, 'no')
    car_service.add_car('3', 'Volkswagen', 2000, 1000000, 'yes')
    car_service.add_car('4', 'Opel Astra', 2005, 950000, 'no')
    car_service.add_car('5', 'Peugeot', 2020, 100000, 'yes')


def test_card_service():
    card_repo = JsonRepository('test_card_service.json')
    undo_redo_service = UndoRedoService()
    card_service = ClientCardService(card_repo,
                                     undo_redo_service)

    card_service.add_card('1', 'Popa', 'Dan', '6020326070912',
                          '26/3/2002', '12/5/2020')
    assert card_service.get_all() == \
           [ClientCard(id_entity='1', last_name='Popa',
                       first_name='Dan',
                       CNP='6020326070912',
                       birthday='26/3/2002',
                       registration_date='12/5/2020')]

    card_service.update_card('1', 'Hritac', 'Dan', '6020326070912',
                             '26/3/2002', '12/7/2020')
    assert card_service.get_all() == \
           [ClientCard(id_entity='1', last_name='Hritac',
                       first_name='Dan',
                       CNP='6020326070912',
                       birthday='26/3/2002',
                       registration_date='12/7/2020')]

    card_service.delete_card('1')
    assert card_service.get_all() == []
    card_service.add_card('1', 'Popa', 'Dan', '6020326070912',
                          '26/3/2002', '12/5/2020')
    assert card_service.handle_search('Popa') == \
           [ClientCard(id_entity='1', last_name='Popa',
                       first_name='Dan',
                       CNP='6020326070912',
                       birthday='26/3/2002',
                       registration_date='12/5/2020')]

    card_service.add_card('2', 'Hritac', 'Rodica', '6601225849274',
                          '25/12/1960', '22/8/2016')
    card_service.add_card('3', 'Scripcariu', 'Marcel', '1283647390212',
                          '20/1/1972', '20/3/2012')
    card_service.add_card('4', 'Dima', 'Maria', '2374658392848',
                          '23/8/1992', '12/5/2017')


def test_transaction_service():
    car_repo = JsonRepository('test_car_service.json')
    transaction_repo = JsonRepository('test_transaction_service.json')
    card_repo = JsonRepository('test_card_service.json')
    undo_redo_service = UndoRedoService()
    transaction_service = TransactionService(transaction_repo,
                                             car_repo,
                                             card_repo,
                                             undo_redo_service)

    date_time1 = \
        str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
    transaction_service.add_transaction('1', '1', '1',
                                        100, 50, date_time1)
    assert transaction_service.get_all() == \
           [Transaction(id_entity='1',
                        id_car='1',
                        id_client_card='1',
                        parts_price=100,
                        workmanship_price=45,
                        date_time=date_time1)]

    transaction_service.update_transaction('1', '1', '1',
                                           200, 50, date_time1)
    assert transaction_service.get_all() == \
           [Transaction(id_entity='1',
                        id_car='1',
                        id_client_card='1',
                        parts_price=200,
                        workmanship_price=50,
                        date_time=date_time1)]

    transaction_service.delete_transaction('1')
    assert transaction_service.get_all() == []
    transaction_service.add_transaction('1', '1',
                                        '2', 100, 50, date_time1)
    transaction_service.add_transaction('2', '3',
                                        '4', 500, 300, date_time1)
    transaction_service.add_transaction('3', '2',
                                        '1', 200, 500, date_time1)
    transaction_service.add_transaction('4', '1',
                                        '', 1030, 850, date_time1)
    transaction_service.add_transaction('5', '4',
                                        '', 980, 1000, date_time1)
    res = transaction_service.transaction_in_interval(100, 700)
    assert res == \
           [Transaction(id_entity='1', id_car='1', id_client_card='2',
                        parts_price=100, workmanship_price=45.0,
                        date_time=date_time1),
            Transaction(id_entity='2', id_car='3', id_client_card='4',
                        parts_price=0, workmanship_price=270.0,
                        date_time=date_time1),
            Transaction(id_entity='3', id_car='2', id_client_card='1',
                        parts_price=200, workmanship_price=450.0,
                        date_time=date_time1)]

    assert transaction_service.descending_order_car() == \
           [Car(id_entity='4', model='Opel Astra',
                purchase_year=2005, km_number=950000,
                assurance='no'),
            Car(id_entity='1', model='Dacia',
                purchase_year=2012, km_number=700000,
                assurance='no'),
            Car(id_entity='2', model='Skoda',
                purchase_year=2017, km_number=600000,
                assurance='no'),
            Car(id_entity='3', model='Volkswagen',
                purchase_year=2000, km_number=1000000,
                assurance='yes')]

    for i in transaction_service.descending_order_card():
        print(i)

    date = datetime.date.today().strftime("%d/%m/%Y")
    transaction_service.delete_between_days('12/5/2012', date)
    assert transaction_service.get_all() == []


def test_all_service():
    clear_file('test_car_service.json')
    clear_file('test_card_service.json')
    clear_file('test_transaction_service.json')
    test_car_service()
    test_card_service()
    test_transaction_service()
