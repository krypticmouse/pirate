from pydantic import BaseModel
from typing import Optional, Union

from pirate.models import Encoder
from pirate.models.types import Sampling
from pirate.retrievers import BaseRetriever
from pirate.data import (
    Passages,
    Queries,
    Triples,
)

class MiningParams(BaseModel):
    passages: Passages
    queries: Queries
    triples: Triples

class ScoreThresholdMinerParams(MiningParams):
    threshold: float = 0.8
    top_k: Optional[int] = None

    model: Union[BaseRetriever, Encoder]
    sampling: Sampling = Sampling.RANDOM