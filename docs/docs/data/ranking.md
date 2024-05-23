# Ranking Class

The `Ranking` class is designed to handle ranking data in different formats such as JSON, JSONL, and CSV. It provides methods to load rankings from files or lists, save rankings to files, and access individual rankings. Current there is no way to pass a dictionary of ranking, but there might be in the future.

## Loading Rankings

To load rankings into a `Ranking` object, you can provide the data in one of three formats:

1. **File Path**: Pass the path to a file containing the ranking data. The file should be in a supported format such as JSON, JSONL, or CSV.

2. **List**: Pass a list of ranking tuples, where each tuple represents a single ranking and contains the necessary fields such as `qid` and `ranking`.

Here is an example of loading rankings from a file:

```python
from pirate.data import Ranking

# Load rankings from a JSON file
rankings = Ranking("rankings.jsonl")
```

## Saving Rankings

You can save the loaded rankings to a JSON or CSV file using the `save()` method. By default, the data will be saved in JSON format, but you can specify the file format using the `format` parameter.

Here is an example of saving rankings to a CSV file:

```python
from pirate.data import Ranking

# Load rankings from a JSON file
rankings = Ranking("rankings.jsonl")

# Save rankings to a CSV file
rankings.save("rankings.csv")
```

## Accessing Rankings

Once rankings are loaded into a `Ranking` object, you can access individual rankings using their indices. The `Ranking` class provides list-like indexing, allowing you to retrieve specific rankings based on their position in the list.

Here is an example of accessing a ranking by its index:

```python
# Access a specific ranking by its index
ranking = rankings[0]
```

## Getting a Passage Group for a Query

You can get a list of ranked passages for a query by passing the query ID to the `get_passage_groups()` method. This will return a `pl.DataFrame` with pasasges for the query ranked in the order specified in the ranking data.

Here is an example of getting a passage group for a query:

```python
# Get the passage group for a query
passage_grp = rankings.get_passage_groups("123")
```

## Iterating Over Rankings

You can iterate over rankings using a `for` loop, which will iterate over each ranking in the order they were loaded. Here is an example of iterating over rankings:

```python
for ranking in rankings:
    print(ranking)
```