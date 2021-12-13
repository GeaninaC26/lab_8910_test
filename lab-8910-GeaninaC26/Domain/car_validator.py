from Domain.car import Car


class CarValidator:
    def validate_car(self, car: Car):
        # validates fields for car
        # purchase year and km should be positives
        # assurance should be either yes or no
        errors = []
        if int(car.purchase_year) <= 0:
            errors.append('anul achizitiei '
                          'trebuie sa fie pozitiv')
        if int(car.km_number) <= 0:
            errors.append('km trebuie sa fie pozitivi')
        if car.assurance not in ['yes', 'no']:
            errors.append('garantia trebuie sa fie yes or no')
        if errors:
            raise ValueError(errors)
