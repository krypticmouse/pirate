import random

from tqdm import tqdm
from typing import List, Optional

from pirate.data import Triples
from pirate.miner.base import BaseMiner
from pirate.models import InBatchMinerParams

class InBatchMiner(BaseMiner):
    def __init__(self, mining_params: InBatchMinerParams):
        super().__init__(mining_params)
        
        self.mining_params = mining_params
        self.triples = self.mining_params.triples
        
        assert self.triples is not None, "Triples must be provided."
        assert len(self.triples) > 0, "Triples must not be empty."
        assert max([len(i) for i in self.triples]) == 2, "Triples must be in the pair format [qid, pid]."


    def mine(
        self,
        num_negs_per_pair: int = 1,
        exclude_pairs: Optional[List[List[str]]] = None
    ) -> Triples:
        triples_list = []
        for qid, pos_pid in tqdm(self.triples, desc="Mining in-batch negatives", total=len(self.triples), disable=self.mining_params.verbose):
            if exclude_pairs and [qid, pos_pid] in exclude_pairs:
                continue
            
            other_pos_pids = [pid for q, pid in self.triples if q != qid]
            
            random_negative_passages = random.sample(other_pos_pids, num_negs_per_pair)
            
            for neg_pid in random_negative_passages:
                triples_list.append([qid, pos_pid, neg_pid])
        
        triples = Triples(triples_list)
        return triples
