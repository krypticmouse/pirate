import random
from typing import List, Optional

from tqdm import tqdm

from pirate.data import (
    Passages,
    Queries,
    Triples
)
from pirate.models import (
    Encoder, 
    Sampling,
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

        self.triples = self.sampling_params.triples

        assert self.triples is not None, "Triples must be provided."
        assert len(self.triples) > 0, "Triples must not be empty."
        assert max([len(i) for i in self.triples]) == 2, "Triples must be in the pair format [qid, pid]."

        passage_dict = {}
        query_dict = {}
        for qid, pid in self.triples:
            assert qid in self.sampling_params.queries, f"Query {qid} not found."
            assert pid in self.sampling_params.passages, f"Passage {pid} not found."

            passage_dict[pid] = self.sampling_params.passages[pid]
            query_dict[qid] = self.sampling_params.queries[qid]
            
        self.passages = Passages(passage_dict)
        self.queries = Queries(query_dict)

        self.encoder = self._get_model()

        self._seed()

    def _seed(self):
        if self.sampling_params.seed is not None:
            random.seed(self.sampling_params.seed)
        
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
        exclude_pairs: Optional[List[List[str]]] = None
    ) -> Triples:
        self.encoder.index(self.passages)
        rankings = self.encoder.rank(self.queries, self.sampling_params.top_k)

        triples_list = []
        for qid, pos_pid in tqdm(self.triples, desc="Mining hard negatives", total=len(self.triples), disable=self.sampling_params.verbose):
            if exclude_pairs and [qid, pos_pid] in exclude_pairs:
                continue
            
            passage_groups = rankings.get_passage_groups(qid)["pid"].to_list()
            
            passage_sample_set = []
            match self.sampling_params.sampling:
                case Sampling.RANDOM:
                    passage_sample_set = passage_groups
                case Sampling.RTOP_K:
                    passage_sample_set = passage_groups[:self.sampling_params.top_k] if self.sampling_params.top_k else passage_groups

            random_negative_passages = random.sample(passage_sample_set, num_negs_per_pair)

            for neg_pid in random_negative_passages:
                triples_list.append([qid, pos_pid, neg_pid])

        triples = Triples(triples_list)
        return triples