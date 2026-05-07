from abc import ABC, abstractmethod
from typing import Any


class BasePipeline(ABC):
    @abstractmethod
    def validate_input(self, payload: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def generate(self, payload: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def simulate(self, payload: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def score(self, payload: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def critique(self, payload: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def optimize(self, payload: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    def build_output(self, payload: Any) -> dict:
        raise NotImplementedError
