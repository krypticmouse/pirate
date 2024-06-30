from enum import Enum


class Encoder(str, Enum):
    BIENCODER = "bi-encoder"
    CROSSENCODER = "cross-encoder"
    BM25 = "bm25"
    BM25L = "bm25l"
    BM25PLUS = "bm25+"


class Sampling(str, Enum):
    RANDOM = "random"
    RTOP_K = "rtop-k"


class Miners(str, Enum):
    IN_BATCH_MINER = "in-batch"
    HARD_MINER = "hard"
    SYNTHETIC_SHALLOW_MINER = "synthetic-shallow"
    SYNTHETIC_DEEP_MINER = "synthetic-deep"
    TRISAMPLER = "trisampler"


class SyntheticPipelineType(str, Enum):
    SHALLOW = "shallow"
    DEEP = "deep"
