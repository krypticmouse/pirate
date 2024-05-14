import pytest
from pirate.retrievers.bm25 import BM25Retriever
from pirate.models.types import Encoder
from pirate.data import Passages, Queries

@pytest.fixture
def sample_passages():
    return Passages([
        "This is the first passage",
        "This is the second passage",
        "This is the third passage"
    ])

@pytest.fixture
def sample_queries():
    return Queries([
        "first passage",
        "second passage",
        "fourth passage"
    ])

def test_bm25_init():
    retriever = BM25Retriever(Encoder.BM25)

    assert retriever.model_name == Encoder.BM25
    assert retriever.tokenizer("test string") == ["test", "string"]

def test_bm25_index(sample_passages):
    retriever = BM25Retriever(Encoder.BM25)
    retriever.index(sample_passages)

    assert retriever.indexed_corpus is not None
    assert len(retriever.index_id_lookup) == len(sample_passages)

def test_bm25_rank(sample_passages, sample_queries):
    retriever = BM25Retriever(Encoder.BM25)
    retriever.index(sample_passages)
    
    ranking = retriever.rank(sample_queries)
    assert len(ranking) == len(sample_queries) * len(sample_passages)

    top_2_ranking = retriever.rank(sample_queries, top_k=2)
    assert len(top_2_ranking) == len(sample_queries) * 2

def test_invalid_index_corpus():
    retriever = BM25Retriever(Encoder.BM25)
    with pytest.raises(ValueError):
        retriever.index(["invalid", "corpus", "type"])

def test_rank_before_index():
    retriever = BM25Retriever(Encoder.BM25)
    with pytest.raises(ValueError):
        retriever.rank(Queries(["test"]))
