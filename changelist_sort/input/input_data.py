"""Valid Input Data Class.
"""
from dataclasses import dataclass

from changelist_data.storage import ChangelistDataStorage

from changelist_sort.sorting.sort_mode import SortMode


@dataclass(frozen=True)
class InputData:
    """A Data Class Containing Program Input.

    Fields:
    - storage (ChangelistDataStorage): The Changelist Data Storage.
    - sort_mode (SortMode): The selected Sorting Mode enum value.
    - remove_empty (bool): Whether to remove empty changelists after sort.
    """
    storage: ChangelistDataStorage
    sort_mode: SortMode = SortMode.MODULE
    remove_empty: bool = False
