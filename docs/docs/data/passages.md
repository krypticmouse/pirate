# Passages

The `Passages` class in Pirate is used to handle and manipulate text data in the form of passages. It inherits from the `BaseData` class and provides additional functionality specific to working with passages.

## Use Case

The `Passages` class is particularly useful when you have a collection of text passages that you want to load, process, and manipulate. It supports loading data from various sources such as JSON files, CSV files, lists, and dictionaries. This flexibility allows you to work with passage data regardless of its original format.

Some common use cases for the `Passages` class include:

- Loading and preprocessing a dataset of text passages for further analysis or mining.
- Extracting specific passages based on certain criteria or conditions.
- Performing text-based operations on the loaded passages, such as filtering, transforming, or aggregating.

## Module Overview

The `Passages` class provides the following key features:

- **Initialization:** You can create a `Passages` object by passing the data source (file path, list, or dictionary) along with optional parameters for specifying the ID key and content key.
- **Data Loading:** The class supports loading passage data from JSON files, CSV files, lists, and dictionaries. It automatically determines the appropriate loading method based on the input format.
- **Data Saving:** You can save the passage data to JSON or CSV files using the `save()` method.
- **Data Access:** The loaded passages can be accessed using dictionary-like syntax, allowing you to retrieve specific passages by their ID or index.
- **Iteration:** The `Passages` object is iterable, enabling you to loop over the loaded passages easily.

## Loading Passages

To load passages into a `Passages` object, you can provide the data in one of three formats:

1. **File Path**: Pass the path to a file containing the passage data. The file should be in a supported format such as JSON or CSV.

2. **List**: Pass a list of passage dictionaries, where each dictionary represents a single passage and contains the necessary fields for id and content.

3. **Dictionary**: Pass a dictionary where the keys are passage IDs and the values are the corresponding passage contents.

Here is an example of loading passages from a file:

```python
from pirate.data import Passages

# Load passages from a JSON file
passages = Passages("passages.json")
```

By default for JSON files and dictionaries, the `Passages` class assumes that the passage data contains fields named `pid` and `content` for each passage. However, you can specify custom ID and content keys when initializing the `Passages` object if your data has different field names.

Here is an example of loading passages with custom ID and content keys:

```python
from pirate.data import Passages

# Load passages with custom ID and content keys
passages = Passages("passages.json", id_key="passage_id", content_key="passage_text")
```

Once passages are loaded into a `Passages` object, you can access individual passages using their IDs or indices. The `Passages` class provides a dictionary-like interface for accessing passages, making it easy to retrieve specific passages based on their IDs.

Here is an example of accessing a passage by its ID:

```python
# Access a specific passage by its ID
passage = passages["123"]
```

## Saving Passages

You can save the loaded passages to a JSON or CSV file using the `save()` method. By default, the data will be saved in JSON format, but you can specify the file format using the `format` parameter.

Here is an example of saving passages to a CSV file:

```python
from pirate.data import Passages

# Load passages from a JSON file
passages = Passages("passages.json")

# Save passages to a CSV file
passages.save("passages.csv")
```

## Iterating Over Passages

The `Passages` object is iterable, which means you can easily loop over the loaded passages using a `for` loop. This allows you to perform operations on each passage or extract specific information from the passages.

Here is an example of iterating over the loaded passages:

```python
from pirate.data import Passages

# Load passages from a JSON file
passages = Passages("passages.json")

# Iterate over the loaded passages
for id in passages:
    print(id, passage[id])
```
