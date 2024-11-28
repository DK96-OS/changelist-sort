""" Sort With Developer File Patterns.
"""
from changelist_sort import list_key
from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.list_key import ListKey
from changelist_sort.sorting import file_sort, module_sort
from changelist_sort.sorting.module_type import ModuleType
from changelist_sort.sorting.sorting_changelist import SortingChangelist
from changelist_sort.sorting.sorting_file_pattern import SortingFilePattern


_SRC_DIR_PATTERN = SortingFilePattern(first_dir='changelist_sort')
_TEST_DIR_PATTERN = SortingFilePattern(first_dir='test')
_INPUT_PACKAGE_PATTERN = SortingFilePattern(path_end='input')
_SORTING_PACKAGE_PATTERN = SortingFilePattern(path_end='sorting')
_WORKSPACE_PACKAGE_PATTERN = SortingFilePattern(path_end='workspace')

_BUILD_UPDATES_KEY = list_key.compute_key('Build Updates')

# Modify these Patterns
DEVELOPER_CL_TUPLE: tuple[SortingChangelist, ...] = (
    SortingChangelist(
        None,
        list_key.compute_key('Documentation'),
        [
            SortingFilePattern(
                file_ext='md',
            ),
        ]
    ),
    SortingChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Input Package Tests'),
        [
            _TEST_DIR_PATTERN,
            _INPUT_PACKAGE_PATTERN,
        ]
    ),
    SortingChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Sorting Package Tests'),
        [
            _TEST_DIR_PATTERN,
            _SORTING_PACKAGE_PATTERN,
        ]
    ),
    SortingChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Workspace Package Tests'),
        [
            _TEST_DIR_PATTERN,
            _WORKSPACE_PACKAGE_PATTERN,
        ]
    ),
    # Tests that don't match a pattern
    SortingChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Tests'),
        [
            _TEST_DIR_PATTERN,
        ]
    ),
    SortingChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Input Package'),
        [
            _SRC_DIR_PATTERN,
            _INPUT_PACKAGE_PATTERN,
        ]
    ),
    SortingChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Sorting Package'),
        [
            _SRC_DIR_PATTERN,
            _SORTING_PACKAGE_PATTERN,
        ]
    ),
    SortingChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Workspace Package'),
        [
            _SRC_DIR_PATTERN,
            _WORKSPACE_PACKAGE_PATTERN,
        ]
    ),
    SortingChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Main Package Source'),
        [
            _SRC_DIR_PATTERN,
        ]
    ),
    SortingChangelist(
        ModuleType.ROOT,
        list_key.compute_key('Shell Scripts'),
        [
            SortingFilePattern(
                file_ext='sh',
            ),
        ]
    ),
    SortingChangelist(
        ModuleType.ROOT,
        list_key.compute_key('Project Root'),
        [
            SortingFilePattern(
                inverse=True,
                first_dir='gradle',
            ),
            SortingFilePattern(
                inverse=True,
                file_ext='gradle',
            ),
            SortingFilePattern(
                inverse=True,
                file_ext='kts',
            ),
        ]
    ),
    SortingChangelist(
        ModuleType.GRADLE,
        _BUILD_UPDATES_KEY,
        [
            SortingFilePattern(
                inverse=True,
                first_dir='gradle',
            ),
            SortingFilePattern(
                inverse=True,
                first_dir='',
            ),
        ]
    ),
    SortingChangelist(
        ModuleType.ROOT,
        _BUILD_UPDATES_KEY,
        [
            SortingFilePattern(file_ext='gradle'),
        ]
    ),
    SortingChangelist(
        ModuleType.ROOT,
        _BUILD_UPDATES_KEY,
        [
            SortingFilePattern(file_ext='properties'),
        ]
    ),
    SortingChangelist(
        ModuleType.GRADLE,
        list_key.compute_key('Module Gradle Build Files'),
        [
            SortingFilePattern(
                inverse=True,
                first_dir='gradle',
            ),
            SortingFilePattern(
                inverse=True,
                first_dir='',
            ),
        ]
    ),
)


def filter_patterns_by_module(
    module_type: ModuleType | None
) -> list[SortingChangelist]:
    """ Filter the Changelists by the ModuleType their Pattern applies to.
    """
    return list(filter(
        lambda dcl: dcl.module_type is None or dcl.module_type == module_type,
        DEVELOPER_CL_TUPLE
    ))


def sort_file_by_developer(
    cl_map: ChangelistMap,
    file: ChangeData,
) -> bool:
    """
    Apply the Developer FilePattern Setting to Sort a single File into the Changelist Map.
    - Filters Patterns by matching ModuleType before checking files.
    - Fallback to Module Sort
    """
    # Filter Developer Changelist Tuple by File's ModuleType 
    filtered_dcl_patterns = filter_patterns_by_module(file_sort.get_module_type(file))
    # Check Developer Changelists in Tuple Order
    for dcl_pattern in filtered_dcl_patterns:
        if dcl_pattern.check_file(file):
            # Pattern Matched.
            # Search Map. Add File to Changelist.
            if (cl := cl_map.search(dcl_pattern.list_key.key)) is not None:
                cl.changes.append(file)
                return True
            # Create the Developer Changelist. Add File to Changelist.
            cl_map.create_changelist(dcl_pattern.list_key.changelist_name).changes.append(file)
            return True
    # Fallback to Module Sort when Developer Sort Fails.
    return module_sort.sort_file_by_module(cl_map, file)


def is_sorted_by_developer(
    changelist_key: ListKey,
    file: ChangeData,
) -> bool:
    """
    Determines if this File matches the ChangeList Key or Name.
    - Finds the First DeveloperChangelist Pattern that matches
    - Fallback to Module Sort
    """
    # Filter Developer Changelist Tuple by File's ModuleType 
    filtered_dcl_patterns = filter_patterns_by_module(file_sort.get_module_type(file))
    # Check Developer Changelists in Tuple Order
    for dcl_pattern in filtered_dcl_patterns:
        if dcl_pattern.check_file(file):
            # Pattern Matched
            if dcl_pattern.list_key.key == changelist_key.key or\
                dcl_pattern.list_key.changelist_name == changelist_key.changelist_name:
                return True
            # This File could be sorted higher in the Developer Changelist order.
            return False
    # Fallback to Module Sort.
    return module_sort.is_sorted_by_module(changelist_key, file)
