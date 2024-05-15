from typing import List

from pirate.data.triples import Triples
from pirate.models import (
    Encoder, 
    ScoreThresholdMinerParams
)
from pirate.retrievers import (
    BaseRetriever,
    BM25Retriever,
    BiEncoder,
    CrossEncoder
)

class ScoreThresholdMiner:
    def __init__(self, sampling_params: ScoreThresholdMinerParams):
        self.sampling_params = sampling_params

        self.encoder = self._get_model()
        
    def _get_model(self) -> BaseRetriever:
        model = self.sampling_params.model

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

    def mine(
        self,
        num_negs_per_pair: int = 1,
        exclude_pairs: List[List[str]] = []
    ) -> Triples:
        rankings = self.encoder.rank(self.passages, self.queries, self.sampling_params.top_k)

        triples = []