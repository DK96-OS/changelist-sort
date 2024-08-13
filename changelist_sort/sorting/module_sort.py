""" Sorting By Module.
    An option of SortMode.
"""
from changelist_sort.sorting import file_sort
from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.sorting.module_type import ModuleType, get_cl_simple_names


def sort_file_by_module(
    cl_map: ChangelistMap,
    file: ChangeData,
) -> bool:
    """
    Sort files into Changelists by Module.

    Parameters:
    - cl_map (ChangelistMap): The Map of Changelists to sort into.
    - file (ChangeData): The File change data to be sorted.

    Returns:
    bool - True when the operation succeeds.
    """
    module_type = file_sort.get_module_type(file)
    if module_type is None:
        return False
    
    file_module = file_sort.get_module_name(file)
    if file_module is None or len(file_module) == 0:
        return False
    # 
    if (cl := cl_map.search(file_module)) is not None:
        cl.changes.append(file)
        return True
    # Create Changelist and Append File ChangeData
    new_cl_name = file_module
    if new_cl_name == 'gradle':
        new_cl_name = 'Build Updates'
    #
    new_cl = cl_map.create_changelist(
        name=capitalize_words(new_cl_name)
    )
    new_cl.changes.append(file)
    return True


def is_sorted_by_module(
    changelist_name: str,
    file: ChangeData,
) -> bool:
    """
    Determine whether this file belongs in the given Changelist.
        Applies Special Module, and Directory equivalencies.

    Parameters:
    - changelist_name (str): The name of the Changelist, used to determine if the file is sorted.
    - file (ChangeData): The File to compare against the Changelist name.

    Returns:
    bool - Whether this file belongs in this Changelist according to Module sort logic.
    """
    if (module_type := file_sort.get_module_type(file)) == ModuleType.ROOT:
        if changelist_name.startswith(
            get_cl_simple_names(module_type)
        ): return True
        # File Extension Checks
        return file.file_ext.endswith(
            file_sort._GRADLE_FILE_SUFFIXES
        ) and changelist_name.startswith(
            get_cl_simple_names(ModuleType.GRADLE)
        )
    if module_type == ModuleType.GRADLE:
        return changelist_name.startswith(
            get_cl_simple_names(module_type)
        )
    # Starts with or Equals
    return changelist_name.startswith(
        file_sort.get_module_name(file)
    )


def capitalize_words(sentence: str) -> str:
    """
    Uppercase the first letter of every word in the sentence.
    """
    return ' '.join(word.capitalize() for word in sentence.split())
