from enum import Enum

class Encoder(Enum):
    BIENCODER = "bi-encoder"
    CROSSENCODER = "cross-encoder"
    BM25 = "bm25"
    BM25L = "bm25l"
    BM25PLUS = "bm25+"

class Sampling(Enum):
    RANDOM = "random"
    RTOP_K = "rtop-k"

class Miners(Enum):
    IN_BATCH_MINER = "in-batch"
    HARD_MINER = "hard"