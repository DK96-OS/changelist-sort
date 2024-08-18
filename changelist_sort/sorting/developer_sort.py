""" Sort With Developer File Patterns.
"""
from changelist_sort import list_key
from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_map import ChangelistMap
from changelist_sort.list_key import ListKey
from changelist_sort.sorting import file_sort, module_sort
from changelist_sort.sorting.module_type import ModuleType
from changelist_sort.workspace.developer_changelist import DeveloperChangelist
from changelist_sort.workspace.developer_file_pattern import DeveloperFilePattern


_SRC_DIR_PATTERN = DeveloperFilePattern(first_dir='changelist_sort')
_TEST_DIR_PATTERN = DeveloperFilePattern(first_dir='test')
_INPUT_PACKAGE_PATTERN = DeveloperFilePattern(path_end='input')
_SORTING_PACKAGE_PATTERN = DeveloperFilePattern(path_end='sorting')
_WORKSPACE_PACKAGE_PATTERN = DeveloperFilePattern(path_end='workspace')


# Modify these Patterns
DEVELOPER_CL_TUPLE: tuple[DeveloperChangelist, ...] = (
    DeveloperChangelist(
        None,
        list_key.compute_key('Documentation'),
        (
            DeveloperFilePattern(
                file_ext='md',
            ),
        )
    ),
    DeveloperChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Input Package Tests'),
        (
            _TEST_DIR_PATTERN,
            _INPUT_PACKAGE_PATTERN,
        )
    ),
    DeveloperChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Sorting Package Tests'),
        (
            _TEST_DIR_PATTERN,
            _SORTING_PACKAGE_PATTERN,
        )
    ),
    DeveloperChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Workspace Package Tests'),
        (
            _TEST_DIR_PATTERN,
            _WORKSPACE_PACKAGE_PATTERN,
        )
    ),
    # Tests that don't match a pattern
    DeveloperChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Tests'),
        (
            _TEST_DIR_PATTERN,
        )
    ),
    DeveloperChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Input Package'),
        (
            _SRC_DIR_PATTERN,
            _INPUT_PACKAGE_PATTERN,
        )
    ),
    DeveloperChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Sorting Package'),
        (
            _SRC_DIR_PATTERN,
            _SORTING_PACKAGE_PATTERN,
        )
    ),
    DeveloperChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Workspace Package'),
        (
            _SRC_DIR_PATTERN,
            _WORKSPACE_PACKAGE_PATTERN,
        )
    ),
    DeveloperChangelist(
        ModuleType.MODULE,
        list_key.compute_key('Main Package Source'),
        (
            _SRC_DIR_PATTERN,
        )
    ),
    DeveloperChangelist(
        ModuleType.ROOT,
        list_key.compute_key('Project Root'),
        (
            DeveloperFilePattern(
                inverse=True,
                first_dir='gradle',
            ),
            DeveloperFilePattern(
                inverse=True,
                file_ext='gradle',
            ),
            DeveloperFilePattern(
                inverse=True,
                file_ext='kts',
            ),
        )
    ),
    DeveloperChangelist(
        None,
        ListKey('buildupdates', 'Build Updates'),
        (
            DeveloperFilePattern(
                inverse=True,
                first_dir='gradle',
            ),
        )
    ),
    DeveloperChangelist(
        None,
        list_key.compute_key('Module Gradle Build Files'),
        (
            DeveloperFilePattern(
                inverse=True,
                first_dir='gradle',
            ),
            DeveloperFilePattern(
                inverse=True,
                first_dir=None,
            ),
        )
    ),
    DeveloperChangelist(
        ModuleType.ROOT,
        list_key.compute_key('Shell Scripts'),
        (
            DeveloperFilePattern(
                file_ext='sh',
            ),
        )
    ),
)


def _filter_patterns_by_module(
    module_type: ModuleType | None
) -> tuple[DeveloperChangelist]:
    """
    Filter the Changelists by the ModuleType their Pattern applies to.
    """
    return tuple(filter(
        lambda dcl: dcl.module_type is None or dcl.module_type == module_type,
        DEVELOPER_CL_TUPLE
    ))


def sort_file_by_developer(
    cl_map: ChangelistMap,
    file: ChangeData,
) -> bool:
    """
    Apply the Developer FilePattern Setting to Sort a single File into the Changelist Map.

    - Fallback to Module Sort
    """
    file_module_type = file_sort.get_module_type(file)
    for pattern in _filter_patterns_by_module(file_module_type):
        if pattern.check_file(file):
            # Pattern Matched
            if (cl := cl_map.search(pattern.list_key.key)) is not None:
                cl.changes.append(file)
                return True
            cl_map.create_changelist(pattern.list_key.changelist_name).changes.append(file)
            return True
    # Fallback to Module Sort when Developer Sort Fails
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
    file_module_type = file_sort.get_module_type(file)
    filtered_patterns = _filter_patterns_by_module(file_module_type)
    for dc_pattern in filtered_patterns:
        if dc_pattern.check_file(file):
            # Pattern Matched
            if changelist_key.key == dc_pattern.list_key.key or\
                changelist_key.changelist_name == dc_pattern.list_key.changelist_name:
                return True
            else:
                # This File could be sorted up higher in the DeveloperChangelist
                return False
    # Fallback to Module Sort
    return module_sort.is_sorted_by_module(changelist_key, file)
