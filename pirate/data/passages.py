import textwrap
from typing import List, Mapping, Union, Optional

from .base import BaseData

class Passages(BaseData):
    """
    The Passages class inherits from the BaseData class. It is used to handle passages of text data.
    """
    def __init__(
        self,
        data: Union[str, List, Mapping],
        id_key: Optional[str] = None, 
        content_key: Optional[str] = None
    ):
        """
        Initialize the Passages object.

        Args:
            data: The data to be loaded. It can be a string (path to a file), a list, or a dictionary.
            id_key: The key used for the id in the data. Defaults to 'pid'.
            content_key: The key used for the content in the data. Defaults to 'passage'.
        """
        id_key = id_key or "pid"
        content_key = content_key or "passage"
        
        super().__init__(data, id_key, content_key)
    
    def __repr__(self):
        """ Return the string representation of the BaseData object. """
        string = textwrap.dedent(
            f"""Passages(
                data: {len(self.data)} entries
                id_key: {self.id_key}
                content_key: {self.content_key}
            )"""
        )
        
        return string
