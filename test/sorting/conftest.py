import pytest

from changelist_sort.list_key import ListKey
from changelist_sort.sorting import SortingChangelist
from changelist_sort.sorting.module_type import ModuleType
from changelist_sort.sorting.sorting_file_pattern import SortingFilePattern


@pytest.fixture
def shell_scripts_file_pattern():
    return SortingFilePattern(file_ext='sh')


@pytest.fixture
def shell_scripts_changelist(shell_scripts_file_pattern):
    return SortingChangelist(
        module_type=ModuleType.ROOT,
        list_key=ListKey(key='shellscripts', changelist_name='Shell Scripts'),
        file_patterns=[shell_scripts_file_pattern],
    )
