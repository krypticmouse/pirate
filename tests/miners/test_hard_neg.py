import pytest
from pirate.miner.hard_neg import HardNegativesMiner
from pirate.models import HardNegativesMinerParams, Encoder, Sampling
from pirate.data import Passages, Queries, Triples

@pytest.fixture
def example_data():
    passages = Passages({
        "p1": "This is passage 1",
        "p2": "This is passage 2",
        "p3": "This is passage 3"
    })
    queries = Queries({
        "q1": "What is passage 1 about?",
        "q2": "What is passage 2 about?"
    })
    triples = Triples([
        ["q1", "p1"],
        ["q2", "p2"]
    ])
    return passages, queries, triples

def test_hard_neg_miner_init(example_data):
    passages, queries, triples = example_data
    params = HardNegativesMinerParams(
        model=Encoder.BM25,
        sampling=Sampling.RANDOM,
        top_k=5,
        seed=42,
        triples=triples,
        passages=passages,
        queries=queries
    )
    miner = HardNegativesMiner(params)
    assert miner.sampling_params == params
    assert len(miner.sampling_params.triples) == 2
    assert len(miner.sampling_params.passages) == 3
    assert len(miner.sampling_params.queries) == 2

    assert len(miner.triples) == 2
    assert len(miner.passages) == 2
    assert len(miner.queries) == 2

    assert miner.encoder is not None
    assert miner.sampling_params.top_k == 5

    assert miner.triples[0][0] == "q1"
    assert miner.triples[0][1] == "p1"
    assert miner.passages["p1"] == "This is passage 1"
    assert miner.queries["q1"] == "What is passage 1 about?"

def test_hard_neg_miner_init_invalid_triples():
    with pytest.raises(Exception):
        params = HardNegativesMinerParams(
            model=Encoder.BM25,
            sampling=Sampling.RANDOM,
            top_k=5,
            seed=42,
            triples=None,
            passages=Passages({"p1": "passage 1"}),
            queries=Queries({"q1": "query 1"})
        )

        miner = HardNegativesMiner(params)

def test_hard_neg_miner_init_invalid_triple_format():
    with pytest.raises(AssertionError):
        params = HardNegativesMinerParams(
            model=Encoder.BM25,
            sampling=Sampling.RANDOM,
            top_k=5,
            seed=42,
            triples=Triples([["q1", "p1", "p2"]]),
            passages=Passages({"p1": "passage 1"}),
            queries=Queries({"q1": "query 1"})
        )

        miner = HardNegativesMiner(params)

def test_hard_neg_miner_init_invalid_query():
    with pytest.raises(Exception):
        params = HardNegativesMinerParams(
            model=Encoder.BM25,
            sampling=Sampling.RANDOM,
            top_k=5,
            seed=42,
            triples=Triples([["q1", "p1"]]),
            passages=Passages({"p1": "passage 1"}),
            queries=None
        )

        miner = HardNegativesMiner(params)

def test_hard_neg_miner_init_invalid_passage():
    with pytest.raises(Exception):
        params = HardNegativesMinerParams(
            model=Encoder.BM25,
            sampling=Sampling.RANDOM,
            top_k=5,
            seed=42,
            triples=Triples([["q1", "p2"]]),
            passages=None,
            queries=Queries({"q1": "query 1"})
        )

        miner = HardNegativesMiner(params)

def test_hard_neg_miner_mine(example_data):
    passages, queries, triples = example_data  
    params = HardNegativesMinerParams(
        model=Encoder.BM25,
        sampling=Sampling.RANDOM, 
        top_k=5,
        seed=42,
        triples=triples,
        passages=passages,
        queries=queries
    )
    miner = HardNegativesMiner(params)
    mined_triples = miner.mine(num_negs_per_pair=1)
    print(mined_triples)
    assert len(mined_triples) == 2
    assert all(len(t) == 3 for t in mined_triples)

def test_hard_neg_miner_mine_exclude_pairs(example_data):
    passages, queries, triples = example_data
    params = HardNegativesMinerParams(
        model=Encoder.BM25,
        sampling=Sampling.RANDOM,
        top_k=5,
        seed=42,
        triples=triples,
        passages=passages,
        queries=queries
    )
    miner = HardNegativesMiner(params)
    mined_triples = miner.mine(num_negs_per_pair=1, exclude_pairs=[["q1", "p1"]])
    assert len(mined_triples) == 1
    assert mined_triples[0][0] == "q2"

def test_hard_neg_miner_mine_rtop_k_sampling(example_data):
    passages, queries, triples = example_data
    params = HardNegativesMinerParams(
        model=Encoder.BM25,
        sampling=Sampling.RTOP_K,
        top_k=3,
        seed=42,
        triples=triples,
        passages=passages,
        queries=queries
    )
    miner = HardNegativesMiner(params)
    mined_triples = miner.mine(num_negs_per_pair=1)
    assert len(mined_triples) == 2
    assert all(len(t) == 3 for t in mined_triples)
    # Check that negatives are sampled from top k
    for t in mined_triples:
        assert t[2] in passages

def test_hard_neg_miner_mine_empty_triples(example_data):
    passages, queries, _ = example_data

    with pytest.raises(AssertionError):
        params = HardNegativesMinerParams(
            model=Encoder.BM25,
            sampling=Sampling.RANDOM,
            top_k=5,
            seed=42,
            triples=Triples([]),
            passages=passages,
            queries=queries
        )
        miner = HardNegativesMiner(params)
        miner.mine(num_negs_per_pair=1)

def test_hard_neg_miner_mine_invalid_encoder(example_data):
    passages, queries, triples = example_data

    with pytest.raises(ValueError):
        params = HardNegativesMinerParams(
            model="invalid",
            sampling=Sampling.RANDOM,
            top_k=5,
            seed=42,
            triples=triples,
            passages=passages,
            queries=queries
        )
        miner = HardNegativesMiner(params)
        miner.mine(num_negs_per_pair=1)
