from typing import List

from pirate.data.triples import Triples
from pirate.models import (
    Encoder, 
    HardNegativesMinerParams
)
from pirate.retrievers import (
    BaseRetriever,
    BM25Retriever,
    BiEncoder,
    CrossEncoder
)

class HardNegativesMiner:
    def __init__(self, sampling_params: HardNegativesMinerParams):
        self.sampling_params = sampling_params

        self.passages = self.sampling_params.passages
        self.queries = self.sampling_params.queries
        self.triples = self.sampling_params.triples

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

        triples_list = []
        for query_id in self.queries:
            for i, passage_id in enumerate(self.passages):
                pass

        triples = Triples(triples_list)
        return triples