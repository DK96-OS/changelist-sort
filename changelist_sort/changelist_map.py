"""The Changelist Map.
"""
from changelist_sort.changelist_data import ChangelistData


class ChangelistMap:
    """
    The Map containing all of the Changelists.
    """

    def __init__(self):
        self.mapping = {}
        self.changelist_ids = set()
    
    def insert(self, changelist: ChangelistData) -> bool:
        """
        Insert a Changelist into the Map.
            Uses the Changelist Simple name as a key.
        """
        if changelist.id in self.changelist_ids:
            return False
        self.changelist_ids.add(changelist.id)
        self.mapping[changelist.get_simple_name()] = changelist
        return True

    def search(self, key: str) -> ChangelistData | None:
        """
        Search the Map dict for the Changelist with the given simple name.
            Expects the Changelist Simple name to match the key.
        """
        return self.mapping.get(key)

    def contains_id(self, id: str) -> bool:
        """
        Determine whether the Map contains the given id.
        """
        return id in self.changelist_ids

    def get_lists(self) -> list[ChangelistData]:
        """
        Obtain all Changelists in the Map as a List.
        """
        all_lists = []
        all_lists.extend(self.mapping.values())
        return all_lists

    def _generate_new_id(self) -> str:
        """
        Create a new Changelist Id that does not appear in this map.
        """
        from random import choices
        chars = list(_hex_char_generator())
        generate_id = lambda: '-'.join(''.join(choices(chars, k=x)) for x in (8, 4, 4, 4, 12))
        test_id = generate_id()
        while self.contains_id(test_id):
            test_id = generate_id()
        return test_id

    def create_changelist(self, name: str) -> ChangelistData:
        """
        Create a new empty Changelist with a new Id, and insert it into the Map.

        Parameters:
        - name (str): The Name of the new Changelist.

        Returns:
        ChangelistData - The Changelist that was recently created and added to the Map.
        """
        new_cl = ChangelistData(
            id=self._generate_new_id(),
            name=name,
            changes=[]
        )
        self.insert(new_cl)
        return new_cl


def _hex_char_generator():
    """Generator yielding all possible hexadecimal characters."""
    for i in range(16):
        if i < 10:
            yield str(i) # Yield lowercase digits (0-9)
        else:
            yield chr(ord('a') + i - 10) # Yield uppercase letters (A-F)
