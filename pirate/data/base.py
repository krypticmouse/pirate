import json

from abc import ABC
from typing import (
    List,
    Mapping,
    Union,
    Optional
)

class BaseData(ABC):
    """
    BaseData is an abstract base class that provides methods for loading and saving data in different formats.
    """

    def __init__(
        self, 
        data: Union[str, List, Mapping],
        id_key: Optional[str] = None,
        content_key: Optional[str] = None
    ):
        """
        Initialize the BaseData object.

        Args:
            data: The data to be loaded. It can be a string (path to a file), a list, or a dictionary.
            id_key: The key used for the id in the data. Defaults to 'id'.
            content_key: The key used for the content in the data. Defaults to 'content'.
        """
        self.id_key = id_key or "id"
        self.content_key = content_key or "content"

        self.load(data)

    def save(self, path: str):
        """
        Save the data to a file.

        Args:
            path: The path to the file where the data will be saved.

        Raises:
            NotImplementedError: If the file extension is not supported.
        """
        ext = path.split(".")[-1]

        if ext == "json" or ext == "jsonl":
            self._to_json(path)
        elif ext == "csv":
            self._to_csv(path)
        else:
            raise NotImplementedError(f"Extension {ext} not supported")

    def load(self, data: Union[str, List, Mapping]):
        """
        Load data from a file, list, or dictionary.

        Args:
            data: The data to be loaded. It can be a string (path to a file), a list, or a dictionary.

        Raises:
            NotImplementedError: If the data type or file extension is not supported.
        """
        if isinstance(data, str):
            ext = data.split(".")[-1]

            if ext == "json" or ext == "jsonl":
                self.data = self._from_json(data)
            elif ext == "csv":
                self.data = self._from_csv(data)
            else:
                raise NotImplementedError(f"Extension {ext} not supported")
        
        elif isinstance(data, list):
            self.data = self._from_list(data)
        
        elif isinstance(data, dict):
            self.data = self._from_dict(data)

        else:
            raise NotImplementedError(f"Type {type(data)} not supported")

    def _to_json(self, path: str):
        """
        Save the data to a JSON file.

        Args:
            path: The path to the file where the data will be saved.
        """
        with open(path, "w") as f:
            for k, v in self.data.items():
                f.write(json.dumps({self.id_key: k, self.content_key: v}) + "\n")

    def _to_csv(self, path: str):
        """
        Save the data to a CSV file.

        Args:
            path: The path to the file where the data will be saved.
        """
        with open(path, "w") as f:
            for k, v in self.data.items():
                f.write(f"{k},{v}\n")

    def _from_dict(self, data: Mapping) -> Mapping:
        """
        Load data from a dictionary.

        Args:
            data: The dictionary from which the data will be loaded.
        """
        return data

    def _from_list(self, data: List) -> Mapping:
        """
        Load data from a list.

        Args:
            data: The list from which the data will be loaded.
        """

        mapped_data = {}

        if isinstance(data[0], str):
            mapped_data = {i: v for i, v in enumerate(data)}
        elif isinstance(data[0], list):
            mapped_data = {i: v for i, v in data}
        
        return mapped_data

    def _from_json(self, data: str):
        """
        Load data from a JSON file.

        Args:
            data: The path to the JSON file from which the data will be loaded.
        """

        mapped_data = {}

        with open(data, "r") as f:
            for line in f:
                record = json.loads(line)
                mapped_data[record[self.id_key]] = record[self.content_key]

        return mapped_data

    def _from_csv(self, data: str):
        """
        Load data from a CSV file.

        Args:
            data: The path to the CSV file from which the data will be loaded.
        """
        mapped_data = {}

        with open(data, "r") as f:
            for line in f:
                k, v = line.split(",")
                mapped_data[k] = v.strip()
            
        return mapped_data

    def __getitem__(self, key):
        """ Get the value of a key. """
        return self.data[key]

    def __len__(self):
        """ Get the length of the data. """
        return len(self.data)

    def __iter__(self):
        """ Return an iterator over the ranking. """
        return iter(self.data)