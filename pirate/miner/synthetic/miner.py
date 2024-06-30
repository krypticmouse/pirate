import dspy
import inspect

from tqdm import tqdm
from loguru import logger
from typing import List, Optional

from pirate.data.triples import Triples
from pirate.miner.base import BaseMiner
from pirate.miner.synthetic.deep import DeepNegativeGenerator
from pirate.miner.synthetic.shallow import ShallowNegativeGenerator
from pirate.models.mining import SyntheticMinerParams
from pirate.models.types import SyntheticPipelineType


__all__ = ["SyntheticMiner"]


class SyntheticMiner(BaseMiner):
    def __init__(self, mining_params: SyntheticMinerParams):
        super().__init__(mining_params)

        dspy.settings.configure(lm=mining_params.lm)
        self.mining_params = mining_params
        self.triples = self.mining_params.triples

        match self.mining_params.pipeline:
            case SyntheticPipelineType.SHALLOW:
                self.pipeline = ShallowNegativeGenerator()
            case SyntheticPipelineType.DEEP:
                self.pipeline = DeepNegativeGenerator()
            case dspy.Module:
                # Validate that the pipeline's forward method takes 2 arguments
                forward_method = getattr(self.mining_params.pipeline, "forward", None)
                if not callable(forward_method):
                    raise ValueError("The provided pipeline must have a 'forward' method.")
                
                forward_params = inspect.signature(forward_method).parameters
                if len(forward_params) != 2:
                    raise ValueError("The pipeline's forward method must take exactly 2 arguments. (query, positive_document)")

                self.pipeline = self.mining_params.pipeline
            case _:
                raise ValueError("Invalid pipeline type.")

        assert self.triples is not None, "Triples must be provided."
        assert len(self.triples) > 0, "Triples must not be empty."
        assert max([len(i) for i in self.triples]) == 2, "Triples must be in the pair format [qid, pid]."


    def mine(
        self,
        num_negs_per_pair: int = 1,
        exclude_pairs: Optional[List[List[str]]] = None
    ) -> Triples:
        triples_list = []
        for qid, pos_pid in tqdm(self.triples, desc="Generating synthetic negatives", total=len(self.triples), disable=self.mining_params.verbose):
            if exclude_pairs and [qid, pos_pid] in exclude_pairs:
                continue

            query = self.mining_params.queries[qid]
            passage = self.mining_params.passages[pos_pid]

            for _ in range(num_negs_per_pair):
                negative_document = self.pipeline.forward(query, passage)   # type: ignore

                assert isinstance(negative_document, str), "Returned negative document must be a string."

                neg_pid = None
                if negative_document not in self.mining_params.passages:
                    neg_pid = self.mining_params.passages.add(negative_document)
                    logger.debug(f"Added negative document to passages with ID: {neg_pid}")
                else:
                    neg_pid = self.mining_params.passages.get_id(negative_document)

                triples_list.append([qid, pos_pid, neg_pid])

        triples = Triples(triples_list)
        return triples
