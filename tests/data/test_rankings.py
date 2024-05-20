import pytest
from pirate.data import Ranking

@pytest.fixture
def json_ranking():
    json_file = "tests/fixtures/rankings/sample_ranking.jsonl"
    return Ranking(json_file)

@pytest.fixture
def csv_ranking():
    csv_file = "tests/fixtures/rankings/sample_ranking.csv"
    return Ranking(csv_file)

def test_load_ranking_from_list():
    data = [
        ["q1", "p1", 1, 0.9],
        ["q1", "p2", 2, 0.8],
        ["q2", "p3", 1, 0.7],
        ["q2", "p4", 2, 0.6]
    ]
    ranking = Ranking(data)
    assert len(ranking) == 4
    assert ranking.data.shape == (4, 4)
    assert ranking.data.columns == ["qid", "pid", "rank", "score"]

def test_load_ranking_from_file_json(json_ranking):
    assert len(json_ranking) == 4 
    assert json_ranking.data.shape == (4, 4)
    assert json_ranking.data.columns == ["qid", "pid", "rank", "score"]

def test_load_ranking_from_file_csv(csv_ranking):
    assert len(csv_ranking) == 4
    assert csv_ranking.data.shape == (4, 4) 
    assert csv_ranking.data.columns == ["qid", "pid", "rank", "score"]

def test_get_passage_groups(json_ranking):
    groups = json_ranking.get_passage_groups("q1")
    assert len(groups) == 2
    assert groups["pid"].to_list() == ["p1", "p2"]
    assert groups["rank"].to_list() == [1, 2]

def test_save_to_json(tmp_path, json_ranking):
    save_path = str(tmp_path / "ranking.json")
    json_ranking.save(save_path)
    reloaded = Ranking(save_path)
    assert reloaded.data.shape == (4, 4)

def test_save_to_csv(tmp_path, csv_ranking):  
    save_path = str(tmp_path / "ranking.csv")
    csv_ranking.save(save_path)
    reloaded = Ranking(save_path)
    assert reloaded.data.shape == (4, 4)
