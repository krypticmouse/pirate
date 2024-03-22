import pytest
from pirate.data import Triples

@pytest.fixture
def json_triples():
    json_file = "tests/fixtures/triples/sample_triple.jsonl"
    return Triples(json_file)


@pytest.fixture
def csv_triples():
    csv_file = "tests/fixtures/triples/sample_triple.csv"
    return Triples(csv_file)


def test_load_triple_from_list():
    data = [
        ["qid1", "ppid1", "npid1"],
        ["qid2", "ppid2", "npid2"]
    ]
    triples = Triples(data)
    assert triples.triples == data


def test_load_triple_from_file_json(json_triples):
    assert json_triples.triples == [
        ["sample_qid_1", "sample_ppid_1", "sample_npid_1"],
        ["sample_qid_2", "sample_ppid_2", "sample_npid_2"]
    ]


def test_load_triple_from_file_csv(csv_triples):
    assert csv_triples.triples == [
        ["sample_qid_1", "sample_ppid_1", "sample_npid_1"],
        ["sample_qid_2", "sample_ppid_2", "sample_npid_2"]
    ]
