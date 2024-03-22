import pytest
from pirate.data import Queries

@pytest.fixture
def json_queries():
    json_file = "tests/fixtures/queries/sample_query.jsonl"
    return Queries(json_file)


@pytest.fixture
def csv_queries():
    csv_file = "tests/fixtures/queries/sample_query.csv"
    return Queries(csv_file)


def test_load_query_from_list():
    data = [
        "This is a query.",
        "This is another query."
    ]
    queries = Queries(data)
    assert queries.data == {k: v for k, v in enumerate(data)}

    data = [
        ["1", "This is a query."],
        ["2", "This is another query."]
    ]
    queries = Queries(data)
    assert queries.data == {k: v for k, v in data}


def test_load_query_from_dict():
    data = {
        "1": "This is a query.",
        "2": "This is another query."
    }
    queries = Queries(data)
    assert queries.data == data


def test_load_query_from_file_json(json_queries):
    print(json_queries.data)
    assert json_queries.data == {
        "sample_id_1": "Sample query 1 goes here.",
        "sample_id_2": "Sample query 2 goes here."
    }


def test_load_query_from_file_csv(csv_queries):
    assert csv_queries.data == {
        "sample_id_1": "Sample query 1 goes here.",
        "sample_id_2": "Sample query 2 goes here."
    }