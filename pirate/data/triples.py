import json

from typing import List, Union

class Triples:
    """
    Triples is a class that handles triple data in different formats (json, jsonl, csv).
    """

    def __init__(self, triples: Union[str, List[List[str]]]):
        """
        Initialize the Triples object.

        Args:
            triples: The triples to be loaded. It can be a string (path to a file) or a list of triples.
        """
        self.triples = self.load(triples)

    def load(self, triples: Union[str, List[List[str]]]) -> List[List[str]]:
        """
        Load triples from a file or a list.

        Args:
            triples: The triples to be loaded. It can be a string (path to a file) or a list of triples.

        Raises:
            NotImplementedError: If the file extension or data type is not supported.
        """
        if isinstance(triples, str):
            ext = triples.split(".")[-1]

            if ext == "json" or ext == "jsonl":
                return self._from_json(triples)
            elif ext == "csv":
                return self._from_csv(triples)
            else:
                raise NotImplementedError(f"Extension {ext} not supported")

        elif isinstance(triples, list):
            return triples
        else:
            raise NotImplementedError(f"Type {type(triples)} not supported")
    
    def save(self, path: str):
        """
        Save the triples to a file.

        Args:
            path: The path to the file where the triples will be saved.

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
        
    def _from_json(self, path: str) -> List[List[str]]:
        """
        Load triples from a JSON file.

        Args:
            path: The path to the JSON file from which the triples will be loaded.

        Returns:
            A list of triples.
        """
        with open(path, "r") as f:
            return [json.loads(line) for line in f]
    
    def _from_csv(self, path: str) -> List[List[str]]:
        """
        Load triples from a CSV file.

        Args:
            path: The path to the CSV file from which the triples will be loaded.

        Returns:
            A list of triples.
        """
        with open(path, "r") as f:
            return [[item.strip() for item in line.split(",")] for line in f]
    
    def _to_json(self, path: str) -> None:
        """
        Save the triples to a JSON file.

        Args:
            path: The path to the file where the triples will be saved.
        """
        with open(path, "w") as f:
            for triple in self.triples:
                f.write(json.dumps(list(triple)) + "\n")

    def _to_csv(self, path: str) -> None:
        """
        Save the triples to a CSV file.

        Args:
            path: The path to the file where the triples will be saved.
        """
        with open(path, "w") as f:
            for triple in self.triples:
                f.write(f"{','.join(triple)}\n")

    def __getitem__(self, index: int) -> List[str]:
        """ Return the triple at the given index. """
        return self.triples[index]
    
    def __repr__(self):
        """ Return the string representation of the Triples object. """
        return f"Triples({len(self.triples)} triples)"
    
    def __len__(self):
        """ Return the number of triples. """
        return len(self.triples)
    
    def __iter__(self):
        """ Return an iterator over the triples. """
        return iter(self.triples)
