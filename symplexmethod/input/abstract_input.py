from abc import ABC, abstractmethod
from typing import Tuple


class AbstractInput(ABC):

    @abstractmethod
    def read(self) -> Tuple[list[int], list[list[int]], list[int]]:
        raise NotImplementedError()

    @abstractmethod
    def validate(self) -> bool:
        raise NotImplementedError()
