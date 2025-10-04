from enum import Enum, auto
from typing import Union
from flask_babel import gettext as _


class BaseEnum(Enum):
    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> Union[str, auto]:
        return self.value


class Const(BaseEnum):
    TEST = auto()


class ENV(BaseEnum):
    INIT = "APP_ENV"
    PRODUCTION = "prod"
    DEVELOPMENT = "dev"

class CarStatus(Enum):
    SOLD = _('Sold')
    AWAITING_DELIVERY = _('Awaiting Delivery')
    AVAILABLE = _('Available')

class CarSituation(Enum):
    REFURBISHED = _('Refurbished') # リフレッシュ済み
    NOT_REFURBISHED = _('Not Refurbished') # 未リフレッシュ
    REFURBISHED_PENDING_CLEANING = _('Refurbished/Pending Cleaning') # リフレッシュ済・清掃待ち

class TransactionStatus(Enum):
    DEPOSITED = _('Deposited')
    PAID = _('Paid')

class CarBranches(Enum):
    LEXUS = 'Lexus'
    TOYOTA = 'Toyota'
    MAZDA = 'Mazda'
    HONDA = 'Honda'
    NISSAN = 'Nissan'
    SUZUKI = 'Suzuki'
    SUBARU = 'Subaru'
    DAIHATSU = 'Daihatsu'
    MITSUBISHI = 'Mitsubishi'
    ISUZU = 'Isuzu'
    BMW = 'BMW'
    MERCEDES = 'Mercedes-Benz'
    AMG = 'AMG'
    VOLKSWAGEN = 'Volkswagen'
    AUDI = 'Audi'
    MINI = 'Mini'
    PORSCHE = 'Porsche'
    VOLVO = 'Volvo'
    PEUGEOT = 'Peugeot'
    JEEP = 'Jeep'
    FIAT = 'Fiat'
    CHEVROLET = 'Chevrolet'
    FORD = 'Ford'
    LAND_ROVER = 'LandRover'
    ALFA_ROMEO = 'AlfaRomeo'
    HUMMER = 'Hummer'
    RENAULT = 'Renault'

