import pytest
from pirate.data import Passages

@pytest.fixture
def json_passages():
    json_file = "tests/fixtures/passages/sample_passage.jsonl"
    return Passages(
        json_file,
        id_key="pid",
        content_key="content"
    )


@pytest.fixture
def csv_passages():
    csv_file = "tests/fixtures/passages/sample_passage.csv"
    return Passages(csv_file)


def test_load_passage_from_list():
    data = [
        "This is a passage.",
        "This is another passage."
    ]
    passages = Passages(data)
    assert passages.data == {k: v for k, v in enumerate(data)}

    data = [
        ["1", "This is a passage."],
        ["2", "This is another passage."]
    ]
    passages = Passages(data)
    assert passages.data == {k: v for k, v in data}


def test_load_passage_from_dict():
    data = {
        "1": "This is a passage.",
        "2": "This is another passage."
    }
    passages = Passages(data)
    assert passages.data == data


def test_load_passage_from_file_json(json_passages):
    assert json_passages.data == {
        "sample_id_1": "Sample passage 1 goes here.",
        "sample_id_2": "Sample passage 2 goes here."
    }


def test_load_passage_from_file_csv(csv_passages):
    assert csv_passages.data == {
        "sample_id_1": "Sample passage 1 goes here.",
        "sample_id_2": "Sample passage 2 goes here."
    }