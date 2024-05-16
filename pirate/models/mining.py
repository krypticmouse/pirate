from typing import Optional, Union
from pydantic import BaseModel, ConfigDict

from pirate.models import Encoder
from pirate.models.types import Sampling
from pirate.retrievers import BaseRetriever
from pirate.data import (
    Passages,
    Queries,
    Triples,
)

class MiningParams(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    triples: Triples
    verbose: Optional[bool] = False

class HardNegativesMinerParams(MiningParams):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    passages: Passages
    queries: Queries

    top_k: Optional[int] = None
    model: Union[BaseRetriever, Encoder]
    sampling: Sampling = Sampling.RANDOM

    seed: Optional[int] = None

class InBatchNegativesMinerParams(MiningParams):
    seed: Optional[int] = None