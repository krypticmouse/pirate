from abc import ABC, abstractmethod

from pirate.data import (
    Passages,
    Ranking
)


class BaseRetriever(ABC):
    @abstractmethod
    def index(self, corpus: Passages):
        pass

    @abstractmethod
    def rank(self, *args, **kwargs) -> Ranking:
        pass