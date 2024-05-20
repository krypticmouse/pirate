import pytest
from pirate.miner.in_batch_neg import InBatchNegativesMiner
from pirate.models import InBatchNegativesMinerParams
from pirate.data import Triples

@pytest.fixture
def example_data():
    triples = Triples([
        ["q1", "p1"],
        ["q1", "p2"],
        ["q2", "p3"],
        ["q2", "p4"]
    ])
    return triples

def test_in_batch_neg_miner_init(example_data):
    triples = example_data
    params = InBatchNegativesMinerParams(
        seed=42,
        triples=triples,
        verbose=False
    )
    miner = InBatchNegativesMiner(params)
    assert miner.sampling_params == params
    assert len(miner.sampling_params.triples) == 4
    assert len(miner.triples) == 4

    assert miner.triples[0][0] == "q1"
    assert miner.triples[0][1] == "p1"

def test_in_batch_neg_miner_init_invalid_triples():
    with pytest.raises(Exception):
        params = InBatchNegativesMinerParams(
            seed=42,
            triples=None,
            verbose=False
        )
        miner = InBatchNegativesMiner(params)

def test_in_batch_neg_miner_init_invalid_triple_format():
    with pytest.raises(AssertionError):
        params = InBatchNegativesMinerParams(
            seed=42,
            triples=Triples([["q1", "p1", "p2"]]),
            verbose=False
        )
        miner = InBatchNegativesMiner(params)

def test_in_batch_neg_miner_mine(example_data):
    triples = example_data
    params = InBatchNegativesMinerParams(
        seed=42,
        triples=triples,
        verbose=False
    )
    miner = InBatchNegativesMiner(params)
    mined_triples = miner.mine(num_negs_per_pair=1)
    assert len(mined_triples) == 4
    assert all(len(t) == 3 for t in mined_triples)

def test_in_batch_neg_miner_mine_exclude_pairs(example_data):
    triples = example_data
    params = InBatchNegativesMinerParams(
        seed=42,
        triples=triples,
        verbose=False
    )
    miner = InBatchNegativesMiner(params)
    mined_triples = miner.mine(num_negs_per_pair=1, exclude_pairs=[["q1", "p1"]])
    assert len(mined_triples) == 3
    assert ["q1", "p1"] not in [[t[0], t[1]] for t in mined_triples]

def test_in_batch_neg_miner_mine_empty_triples():
    with pytest.raises(AssertionError):
        params = InBatchNegativesMinerParams(
            seed=42,
            triples=Triples([]),
            verbose=False
        )
        miner = InBatchNegativesMiner(params)
        miner.mine(num_negs_per_pair=1)
