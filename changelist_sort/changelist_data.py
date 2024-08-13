"""The Data Class for a ChangeList.
"""
from dataclasses import dataclass
from typing import Callable

from changelist_sort.change_data import ChangeData


@dataclass(frozen=True)
class ChangelistData:
    """
    The complete Data class representing a ChangeList.
    
    Properties:
    - id (str): The unique id of the changelist.
    - name (str): The name of the changelist.
    - changes (list[ChangeData]): The list of file changes in the changelist.
    - comment (str): The comment associated with the changelist.
    - is_default (bool): Whether this is the active changelist.
    """
    id: str
    name: str
    changes: list[ChangeData]
    comment: str = ""
    is_default: bool = False

    def get_simple_name(self):
        """
        Obtain the simplest version of the changelist name.
            Removes all spaces, and select punctuation characters.
            This is a name that can be used as a key.
        """
        translator = str.maketrans('', '', ' :/\\')
        return ''.join(w.lower() for w in self.name.translate(translator).split())
