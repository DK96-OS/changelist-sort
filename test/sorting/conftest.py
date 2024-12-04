import pytest

from changelist_sort.list_key import ListKey, compute_key
from changelist_sort.sorting import SortingChangelist
from changelist_sort.sorting.module_type import ModuleType
from changelist_sort.sorting.sorting_file_pattern import SortingFilePattern


@pytest.fixture
def shell_scripts_file_pattern() -> SortingFilePattern:
    return SortingFilePattern(file_ext='sh')


@pytest.fixture
def shell_scripts_changelist(shell_scripts_file_pattern) -> SortingChangelist:
    return SortingChangelist(
        module_type=ModuleType.ROOT,
        list_key=ListKey(key='shellscripts', changelist_name='Shell Scripts'),
        file_patterns=[shell_scripts_file_pattern],
    )


@pytest.fixture
def sort_config_empty() -> SortingChangelist:
    return SortingChangelist(
        module_type=None,
        list_key=compute_key(''),
        file_patterns=[],
    )


@pytest.fixture
def sort_config_all() -> SortingChangelist:
    return SortingChangelist(
        module_type=None,
        list_key=compute_key('all'),
        file_patterns=[
            SortingFilePattern(inverse=True)
        ],
    )


@pytest.fixture
def sort_config_root_markdown_docs() -> list[SortingChangelist]:
    return [
        SortingChangelist(
            module_type=ModuleType.ROOT,
            list_key=compute_key('documentation'),
            file_patterns=[
                SortingFilePattern(file_ext='md'),
            ],
        ),
    ]


@pytest.fixture
def sort_config_github_workflows_yml() -> list[SortingChangelist]:
    return [
        SortingChangelist(
            module_type=None,
            list_key=ListKey('githubworkflows', 'GitHub Workflows'),
            file_patterns=[
                SortingFilePattern(first_dir='.github'),
                SortingFilePattern(path_end='workflows'),
                SortingFilePattern(path_end='workflows/'),
                SortingFilePattern(file_ext='yml'),
            ],
        ),
    ]


@pytest.fixture
def sort_config_github_workflows_yml_2() -> list[SortingChangelist]:
    return [
        SortingChangelist(
            module_type=ModuleType.HIDDEN,
            list_key=compute_key('github_workflows'),
            file_patterns=[
                SortingFilePattern(path_start='.github/workflows/'),
                SortingFilePattern(path_start='.github/workflows'),
                SortingFilePattern(path_start='/.github/workflows'),
                SortingFilePattern(file_ext='.yml'),
            ],
        ),
    ]


@pytest.fixture
def sort_config_python_test_files() -> list[SortingChangelist]:
    return [
        SortingChangelist(
            module_type=ModuleType.MODULE,
            list_key=compute_key('Test Files'),
            file_patterns=[
                SortingFilePattern(filename_prefix='test'),
                SortingFilePattern(file_ext='py'),
            ],
        ),
    ]


@pytest.fixture
def sort_config_python_reader_files() -> list[SortingChangelist]:
    """ Matches Python files with names ending "reader".
    """
    return [
        SortingChangelist(
            module_type=ModuleType.MODULE,
            list_key=compute_key('Python Reader Files'),
            file_patterns=[
                SortingFilePattern(filename_suffix='reader'),
                SortingFilePattern(file_ext='py'),
            ],
        ),
    ]
