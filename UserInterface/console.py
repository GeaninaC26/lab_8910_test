import datetime

from Service.car_service import CarService
from Service.transaction_service import TransactionService
from Service.client_card_service import ClientCardService
from Service.undo_redo_service import UndoRedoService
from utils import my_sorted


class Console:
    def __init__(self,
                 car_service: CarService,
                 client_card_service: ClientCardService,
                 transaction_service: TransactionService,
                 undo_redo_service: UndoRedoService):
        self.car_service = car_service
        self.transaction_service = transaction_service
        self.client_card_service = client_card_service
        self.undo_redo_service = undo_redo_service

    def show_menu(self):
        print('a[car|card|tr] - '
              'adaugare masina sau tranzactie'
              ' sau card client.')
        print('u[car|card|tr] - '
              'update masina sau '
              'tranzactie sau card client.')
        print('d[car|card|tr] - '
              'delete masina sau '
              'tranzactie sau card client.')
        print('s[car|card|tr] - '
              'show all masina sau '
              'tranzactie sau card client.')
        print('search.Cautare string.')
        print('rnd. Genereaza n masini.')
        print('5. Afisarea tranzactiilor cu '
              'suma cuprinsa intr-ul interval'
              'dat de utilizator.')
        print('6. Afisarea masinilor ordonate '
              'descrescator dupa suma. '
              'obtinuta pe manopera')
        print('7. Afișarea cardurilor client '
              'ordonate descrescător după valoarea '
              'reducerilor obținute.')
        print('8. Ștergerea tuturor tranzacțiilor dintr-un'
              ' anumit interval de zile.')
        print('9. Actualizarea garanției la fiecare mașină: '
              'o mașină este în garanție dacă și numai dacă '
              'are maxim 3 ani de la achiziție și '
              'maxim 60 000 de km.')

        print('x. Iesire')

    def run_console(self):
        while True:
            self.show_menu()
            opt = input('Alegeti optiunea: ')

            if opt == 'acar':
                self.handle_add_car()
            elif opt == 'acard':
                self.handle_add_card()
            elif opt == 'atr':
                self.handle_add_transaction()
            elif opt == 'scar':
                self.handle_show_all(self.car_service.get_all())
            elif opt == 'scard':
                self.handle_show_all(self.client_card_service.get_all())
            elif opt == 'str':
                self.handle_show_all(self.transaction_service.get_all())
            elif opt == 'ucar':
                id_car = input("Dati id-ul masinii pe"
                               " care doriti sa o modificati.")
                self.handle_update_car(id_car)
            elif opt == 'ucard':
                id_card = input("Dati id-ul cardului pe"
                                " care doriti sa-l modificati.")
                self.handle_update_card(id_card)
            elif opt == 'utr':
                id_tr = input("Dati id-ul tranzactiei pe"
                              " care doriti sa o modificati.")
                self.handle_update_transaction(id_tr)
            elif opt == 'dcar':
                id_car = input("Dati id-ul masinii pe"
                               " care doriti sa o stergeti.")
                self.handle_delete_car(id_car)
            elif opt == 'dcard':
                id_card = input("Dati id-ul cardului pe"
                                " care doriti sa-l stergeti.")
                self.handle_delete_card(id_card)
            elif opt == 'dtr':
                id_tr = input("Dati id-ul tranzactiei pe"
                              " care doriti sa o stergeti.")
                self.handle_delete_transaction(id_tr)
            elif opt == 'search':
                self.handle_search()
            elif opt == 'rnd':
                n = input('Dati nr: ')
                self.handle_generate_cars(n)
            elif opt == '5':
                self.handle_show_between_range()
            elif opt == '6':
                self.handle_show_descending_car()
            elif opt == '7':
                self.handle_show_descending_card()
            elif opt == '8':
                self.handle_delete_between_days()
            elif opt == '9':
                self.handle_update_assurance()
            elif opt == 'u':
                self.undo_redo_service.do_undo()
            elif opt == 'r':
                self.undo_redo_service.do_redo()
            elif opt == 'x':
                break
            else:
                print('Comanda invalida, reincearca.')

    def handle_add_car(self):
        try:
            id_car = input('Dati id-ul masinii.')
            model = input('Dati modelul masinii.')
            purchase_year = int(input('Dati anul achizitiei'))
            km_number = float(input('Dati nr de km.'))
            assurance = input('Dati starea asigurarii: yes/no')

            self.car_service.add_car(id_car, model,
                                     purchase_year, km_number,
                                     assurance)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_show_all(self, objects):
        for obj in objects:
            print(obj)

    def handle_add_card(self):
        try:
            id_client = input('Dati id-ul cardului.')
            last_name = input('Dati numele clientului.')
            first_name = input('Dati prenumele clientului.')
            cnp = input('Dati CNP-ul clientului.')
            birthday = \
                input('Dati data de nastere a clientului')
            registration_date = \
                input('Dati data inregistrarii clientului.')
            self.client_card_service.add_card(id_client,
                                              last_name,
                                              first_name,
                                              cnp, birthday,
                                              registration_date)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_add_transaction(self):
        try:
            id_transaction = input('Dati id-ul tranzactiei.')
            id_car = input('Dati id-ul masinii.')
            id_client_card = input('Dati id client.')
            parts_price = float(input('Dati pretul pieselor.'))
            workmanship_price = float(input('Dati pretul manoperei.'))
            date_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            self.transaction_service.add_transaction(id_transaction,
                                                     id_car,
                                                     id_client_card,
                                                     parts_price,
                                                     workmanship_price,
                                                     date_time)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_car(self, id_car):
        try:
            model = input("Dati noul model.")
            purchase_year = int(input("Dati noul an."))
            km_number = float(input("Dati nr de km."))
            assurance = input("Dati garantia: yes/no.")
            self.car_service.update_car(id_car, model,
                                        purchase_year, km_number,
                                        assurance)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_card(self, id_card):
        try:
            last_name = input("Dati noul nume.")
            first_name = input("Dati noul prenume.")
            cnp = input("Dati noul CNP.")
            birthday = input("Dati noua data de nastere.")
            registration_date = \
                input("Dati noua data a inregistrarii.")
            self.client_card_service.update_card(id_card,
                                                 last_name,
                                                 first_name,
                                                 cnp, birthday,
                                                 registration_date)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_transaction(self, id_transaction):
        try:
            id_car = input("Dati noul id al masinii.")
            id_card = input("Dati noult id al cardului de client.")
            parts_price = input("Dati noul pret al pieselor.")
            workmanship_price = input("Dati noul pret al manoperei.")
            date_time = \
                datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            self.transaction_service.update_transaction(id_transaction,
                                                        id_car, id_card,
                                                        parts_price,
                                                        workmanship_price,
                                                        date_time)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_delete_car(self, id_car):
        try:
            self.car_service.delete_car(id_car)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_delete_card(self, id_card):
        try:
            self.client_card_service.delete_card(id_card)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_delete_transaction(self, id_tr):
        try:
            self.transaction_service.delete_transaction(id_tr)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_search(self):
        string = input("Dati string")
        for i in self.car_service.handle_search(string):
            print(i)
        for i in self.client_card_service.handle_search(string):
            print(i)

    def handle_generate_cars(self, n):
        self.car_service.handle_generate(n)

    def handle_show_between_range(self):
        low = input('Dati prima data a intervalului')
        high = input('Dati ultima data a intervalului.')
        for i in \
                self.transaction_service.transaction_in_interval(int(low),
                                                                 int(high)):
            print(i)

    def handle_show_descending_car(self):
        for i in self.transaction_service.descending_order_car():
            print(i)

    def handle_show_descending_card(self):
        for i in self.transaction_service.descending_order_card():
            print(i)

    def handle_delete_between_days(self):
        first_day = input('Dati prima data a intervalului')
        last_day = input('Dati ultima data a intervalului.')
        self.transaction_service.delete_between_days(first_day,
                                                     last_day)

    def handle_update_assurance(self):
        self.car_service.update_assurance()
