from enum import Enum, auto
from typing import Union


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
