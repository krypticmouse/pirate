# Queries

The `Queries` class in Pirate is used to handle and manipulate query data. It inherits from the `BaseData` class so in terms of functionalities, usecases and utilities is quite similar.

## Loading Queries

To load queries into a `Queries` object, you can provide the data in one of three formats:

1. **File Path**: Pass the path to a file containing the query data. The file should be in a supported format such as JSON or CSV.

2. **List**: Pass a list of query dictionaries, where each dictionary represents a single query and contains the necessary fields such as `id` and `content`.

3. **Dictionary**: Pass a dictionary where the keys are query IDs and the values are the corresponding query contents.

Here is an example of loading queries from a file:

```python
from pirate.data import Queries

# Load queries from a JSON file
queries = Queries("queries.json")
```

By default for JSON files and dictionaries, the `Queries` class assumes that the query data contains fields named `qid` and `query` for each query. However, you can specify custom ID and content keys when initializing the `Queries` object if your data has different field names.

Here is an example of loading queries with custom ID and content keys:

```python
from pirate.data import Queries

# Load queries with custom ID and content keys
queries = Queries("queries.json", id_key="query_id", content_key="query_text")
```

Once queries are loaded into a `Queries` object, you can access individual queries using their IDs or indices. The `Queries` class provides a dictionary-like interface for accessing queries, making it easy to retrieve specific queries based on their IDs.

Here is an example of accessing a query by its ID:

```python
# Access a specific query by its ID
query = queries["123"]
```

## Saving Queries

You can save the loaded queries to a JSON or CSV file using the `save()` method. By default, the data will be saved in JSON format, but you can specify the file format using the `format` parameter.

Here is an example of saving queries to a CSV file:

```python
from pirate.data import Queries

# Load queries from a JSON file
queries = Queries("queries.json")

# Save queries to a CSV file
queries.save("queries.csv")
```

## Iterating Over Queries

The `Queries` object is iterable, which means you can easily loop over the loaded queries using a `for` loop. This allows you to perform operations on each query or extract specific information from the queries.

Here is an example of iterating over the loaded queries:

```python
from pirate.data import Queries

# Load queries from a JSON file
queries = Queries("queries.json")

# Iterate over the loaded queries
for id in queries:
    print(id, query[id])
```