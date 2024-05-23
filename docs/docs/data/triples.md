# Triples Class

The `Triples` class is designed to handle triple or N-way tuple data in different formats such as JSON, JSONL, and CSV. It provides methods to load triples from files or lists, save triples to files, and access individual triples. These are crucial and pirate relies a lot on them for negative mining.

## What are Triples?

Triples are quite frequently used in Information Retrieval, they are pairs that define the passage that is relevant to a query called **positive passage** and the passage that is not relevant to the query called **negative passage**. The `Triples` class is designed to handle such triple data.

```
[query, positive_passage, negative_passage]

OR

[query_id, positive_passage_id, negative_passage_id]
```

However, you can also load a *n-way tuple* which is a general form of a triple. Instead of have just one negative you can have n-1 negatives, triple is a 2-way tuple in that manner.

```
[query, positive_passage, negative_passage_1, negative_passage_2, negative_passage_3, ...]
```

## Loading Triples

To load triples into a `Triples` object, you can provide the data in one of three formats:

1. **File Path**: Pass the path to a file containing the triple data. The file should be in a supported format such as JSON, JSONL, or CSV.

2. **List**: Pass a list of triple tuples, where each tuple represents a single triple and contains the necessary fields such as `qid`, `positive_pid`, and `negative_pid`.

3. **Dictionary**: Pass a dictionary where the keys are query IDs and the values are the corresponding positive and negative passage IDs.

Here is an example of loading triples from a file:

```python
from pirate.data import Triples

# Load triples from a JSON file
triples = Triples("triples.jsonl")
```

## Saving Triples

You can save the loaded triples to a JSON or CSV file using the `save()` method. By default, the data will be saved in JSON format, but you can specify the file format using the `format` parameter.

Here is an example of saving triples to a CSV file:

```python
from pirate.data import Triples

# Load triples from a JSON file
triples = Triples("triples.jsonl")

# Save triples to a CSV file
triples.save("triples.csv")
```

## Accessing Triples

Once triples are loaded into a `Triples` object, you can access individual triples using their indices. The `Triples` class provides list-like indexing, allowing you to retrieve specific triples based on their position in the list.

Here is an example of accessing a triple by its index:

```python
# Access a specific triple by its index
triple = triples[0]
```

## Iterating Over Triples

The `Triples` object is iterable, allowing you to loop over the loaded triples easily. You can use a `for` loop to iterate over the triples and access each one in turn.

Here is an example of iterating over triples:

```python
# Iterate over the loaded triples
for triple in triples:
    print(triple)
```