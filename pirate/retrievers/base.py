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
    def rank_passages(self, *args, **kwargs) -> Ranking:
        pass