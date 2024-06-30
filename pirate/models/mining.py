import dspy

from typing import Optional, Union
from pydantic import BaseModel, ConfigDict

from pirate.models import Encoder
from pirate.retrievers import BaseRetriever
from pirate.models.types import Sampling, SyntheticPipelineType
from pirate.data import (
    Passages,
    Queries,
    Triples,
)


class MiningParams(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    triples: Triples
    verbose: Optional[bool] = False


class HardMinerParams(MiningParams):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    passages: Passages
    queries: Queries

    model: Union[BaseRetriever, Encoder]
    sampling: Sampling = Sampling.RANDOM

    seed: Optional[int] = None
    top_k: Optional[int] = None
    score_threshold: Optional[float] = 0.7


class InBatchMinerParams(MiningParams):
    seed: Optional[int] = None

class SyntheticMinerParams(MiningParams):
    lm: dspy.LM
    pipeline: Union[dspy.Module, SyntheticPipelineType]

    queries: Queries
    passages: Passages