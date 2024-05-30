import random
from typing import List, Optional

from tqdm import tqdm

from pirate.miner.base import BaseMiner
from pirate.data import (
    Passages,
    Queries,
    Triples
)
from pirate.models import (
    Sampling,
    HardMinerParams
)

class HardMiner(BaseMiner):
    def __init__(self, mining_params: HardMinerParams):
        super().__init__(mining_params)

        self.mining_params = mining_params
        self.triples = self.mining_params.triples

        assert self.triples is not None, "Triples must be provided."
        assert len(self.triples) > 0, "Triples must not be empty."
        assert max([len(i) for i in self.triples]) == 2, "Triples must be in the pair format [qid, pid]."

        passage_dict = {}
        query_dict = {}
        for qid, pid in self.triples:
            assert qid in self.mining_params.queries, f"Query {qid} not found."
            assert pid in self.mining_params.passages, f"Passage {pid} not found."

            passage_dict[pid] = self.mining_params.passages[pid]
            query_dict[qid] = self.mining_params.queries[qid]
            
        self.passages = Passages(passage_dict)
        self.queries = Queries(query_dict)

        self.encoder = self._get_model()
        self._seed()


    def mine(
        self,
        num_negs_per_pair: int = 1,
        exclude_pairs: Optional[List[List[str]]] = None
    ) -> Triples:
        self.encoder.index(self.passages)
        rankings = self.encoder.rank_passages(self.queries, self.mining_params.top_k)

        if self.mining_params.score_threshold:
            rankings = rankings.filter_by_score(self.mining_params.score_threshold)

        triples_list = []
        for qid, pos_pid in tqdm(self.triples, desc="Mining hard negatives", total=len(self.triples), disable=self.mining_params.verbose):
            if exclude_pairs and [qid, pos_pid] in exclude_pairs:
                continue
            
            passage_groups = rankings.get_passage_groups(qid)["pid"].to_list()
            
            passage_sample_set = []
            match self.mining_params.sampling:
                case Sampling.RANDOM:
                    passage_sample_set = passage_groups
                case Sampling.RTOP_K:
                    passage_sample_set = passage_groups[:self.mining_params.top_k] if self.mining_params.top_k else passage_groups

            random_negative_passages = random.sample(passage_sample_set, num_negs_per_pair)

            for neg_pid in random_negative_passages:
                triples_list.append([qid, pos_pid, neg_pid])

        triples = Triples(triples_list)
        return triples