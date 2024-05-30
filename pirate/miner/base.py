import random

from typing import List, Any
from abc import ABC, abstractmethod

from pirate.models import Encoder
from pirate.data.triples import Triples
from pirate.retrievers import (
    BaseRetriever,
    BM25Retriever,
    BiEncoder,
    CrossEncoder
)

class BaseMiner(ABC):
    """
    BaseMiner is an abstract base class that provides methods for mining data.
    """

    def __init__(self, mining_params: Any):
        """
        Initialize the BaseMiner object.

        Args:
            data: The data to be mined.
        """
        self.mining_params = mining_params


    @abstractmethod
    def mine(
        self, 
        num_negs_per_pair: int = 1,
        exclude_pairs: List[List[str]] = [],
        *args,
        **kwargs
    ) -> Triples:
        """
        Mine negative samples from the data.

        Args:
            num_negs_per_pair: The number of negative samples to mine per positive pair.
            exclude_pairs: The pairs to exclude from the negative samples.

        Returns:
            A list of new triples.
        """
        pass


    def _seed(self):
        if self.mining_params.seed is not None:
            random.seed(self.mining_params.seed)
        

    def _get_model(self) -> BaseRetriever:
        model = self.mining_params.model

        match model:
            case Encoder.BM25 | Encoder.BM25L | Encoder.BM25PLUS:
                model = BM25Retriever(model)
            case Encoder.BIENCODER:
                raise ValueError("BiEncoder not supported for mining yet.")
                model = BiEncoder(model)
            case Encoder.CROSSENCODER:
                raise ValueError("CrossEncoder not supported for mining yet.")
                model = CrossEncoder(model)
            case BaseRetriever():
                model = model
            case _:
                raise ValueError("Invalid model.")
            
        return model