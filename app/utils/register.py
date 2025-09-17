from abc import ABC, abstractmethod
from flask import Flask


class Module(ABC):
    @abstractmethod
    def register(self) -> None: ...
