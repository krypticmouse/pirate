import textwrap
import polars as pl

from typing import Union, List

class Ranking:
	"""
	Ranking is a class that handles ranking data in different formats (json, jsonl, csv, list).
	"""
	def __init__(self, ranking: Union[str, List]):
		"""
		Initialize the Ranking object.

		Args:
			ranking: The ranking to be loaded. It can be a string (path to a file) or a list.
		"""
		self.load(ranking)

	def load(self, ranking: Union[str, List]):
		"""
		Load ranking from a file or a list.

		Args:
			ranking: The ranking to be loaded. It can be a string (path to a file) or a list.

		Raises:
			NotImplementedError: If the file extension or data type is not supported.
		"""
		if isinstance(ranking, str):
			ext = ranking.split('.')[-1]

			if ext == 'json' or ext == 'jsonl':
				self.ranking = self.from_json(ranking)
			elif ext == 'csv':
				self.ranking = self.from_csv(ranking)
			else:
				raise NotImplementedError(f"Extension {ext} not supported")

		elif isinstance(ranking, list):
			self.from_list(ranking)
		else:
			raise NotImplementedError(f"Type {type(ranking)} not supported")

	def save(self, path: str):
		"""
		Save the ranking to a file.

		Args:
			path: The path to the file where the ranking will be saved.

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

	def from_json(self, path: str):
		"""
		Load ranking from a JSON file.

		Args:
			path: The path to the JSON file from which the ranking will be loaded.
		"""
		self.data = pl.read_json(path, columns=['qid', 'pid', 'rank', 'score'])

	def from_csv(self, path: str):
		"""
		Load ranking from a CSV file.

		Args:
			path: The path to the CSV file from which the ranking will be loaded.
		"""
		self.data = pl.read_csv(path, columns=['qid', 'pid', 'rank', 'score'])

	def from_list(self, ranking: List):
		"""
		Load ranking from a list.

		Args:
			ranking: The list from which the ranking will be loaded.
		"""
		self.data = pl.DataFrame(ranking, schema=['qid', 'pid', 'rank', 'score'])

	def to_json(self, path: str):
		"""
		Save the ranking to a JSON file.

		Args:
			path: The path to the file where the ranking will be saved.
		"""
		self.data.write_json(path)

	def to_csv(self, path: str):
		"""
		Save the ranking to a CSV file.

		Args:
			path: The path to the file where the ranking will be saved.
		"""
		self.data.write_ndjson(path, include_header=False, seperator=',')

	def __getitem__(self, key):
		""" Return the value of the key. """
		return self.data[key]

	def __repr__(self):
		""" Return the string representation of the Ranking object. """
		string = textwrap.dedent(f"""Ranking(
			data: {len(self.data)} rows
			k: {self.data['rank'].max()}
			num_queries: {self.data['qid'].n_unique()}
			max_score: {self.data['score'].max()}
			min_score: {self.data['score'].min()}
		)""", prefix='	')
		
		return string
	
	def __len__(self):
		""" Return the number of rows in the ranking. """
		return len(self.data)
	
	def __iter__(self):
		""" Return an iterator over the ranking. """
		return iter(self.data)