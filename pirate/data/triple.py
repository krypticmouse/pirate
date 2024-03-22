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
        self.load(triples)

    def load(self, triples: Union[str, List[List[str]]]):
        """
        Load triples from a file or a list.

        Args:
            triples: The triples to be loaded. It can be a string (path to a file) or a list of triples.

        Raises:
            NotImplementedError: If the file extension or data type is not supported.
        """
        if isinstance(triples, str):
            ext = triples.split('.')[-1]

            if ext == 'json' or ext == 'jsonl':
                self.triples = self.from_json(triples)
            elif ext == 'csv':
                self.triples = self.from_csv(triples)
            else:
                raise NotImplementedError(f"Extension {ext} not supported")

        elif isinstance(triples, list):
            self.triples = triples
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
        ext = path.split('.')[-1]

        if ext == 'json' or ext == 'jsonl':
            self.to_json(path)
        elif ext == 'csv':
            self.to_csv(path)
        else:
            raise NotImplementedError(f"Extension {ext} not supported")
        
    def from_json(self, path: str) -> List[List[str]]:
        """
        Load triples from a JSON file.

        Args:
            path: The path to the JSON file from which the triples will be loaded.

        Returns:
            A list of triples.
        """
        with open(path, 'r') as f:
            return [json.loads(line) for line in f]
    
    def from_csv(self, path: str) -> List[List[str]]:
        """
        Load triples from a CSV file.

        Args:
            path: The path to the CSV file from which the triples will be loaded.

        Returns:
            A list of triples.
        """
        with open(path, 'r') as f:
            return [[item.strip() for item in line.split(',')] for line in f]
    
    def to_json(self, path: str):
        """
        Save the triples to a JSON file.

        Args:
            path: The path to the file where the triples will be saved.
        """
        with open(path, 'w') as f:
            for qid, ppid, npid in self.triples:
                f.write(json.dumps([qid, ppid, npid]) + '\n')

    def to_csv(self, path: str):
        """
        Save the triples to a CSV file.

        Args:
            path: The path to the file where the triples will be saved.
        """
        with open(path, 'w') as f:
            for qid, ppid, npid in self.triples:
                f.write(f"{qid},{ppid},{npid}\n")