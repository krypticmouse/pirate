from typing import List
from abc import ABC, abstractmethod

from pirate.data import Triples

class BaseMiner(ABC):
    """
    BaseMiner is an abstract base class that provides methods for mining data.
    """

    def __init__(
        self,
        triples: Triples,
        *args,
        **kwargs
    ):
        """
        Initialize the BaseMiner object.

        Args:
            data: The data to be mined.
        """
        pass

    @abstractmethod
    def mine(
        self, 
        num_negs_per_pair: int = 1,
        exclude_pairs: List[List[str]] = []
    ):
        """
        Mine negative samples from the data.

        Args:
            num_negs_per_pair: The number of negative samples to mine per positive pair.
            exclude_pairs: The pairs to exclude from the negative samples.

        Returns:
            A list of new triples.
        """
        pass