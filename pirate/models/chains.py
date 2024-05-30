from typing import Optional
from pydantic import BaseModel, ConfigDict

from pirate.data.triples import Triples


class MineChainConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    triples: Triples
    verbose: Optional[bool] = False

