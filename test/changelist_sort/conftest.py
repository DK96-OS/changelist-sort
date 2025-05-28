import pytest
from changelist_data import ChangelistDataStorage, new_tree
from changelist_data.xml import workspace
from changelist_data.xml.base_xml_tree import BaseXMLTree

from changelist_sort import list_key
from changelist_sort.list_key import ListKey, compute_key
from changelist_sort.sorting import SortingChangelist
from changelist_sort.sorting.module_type import ModuleType
from changelist_sort.sorting.sorting_file_pattern import SortingFilePattern
from test.conftest import wrap_tree_in_storage, MODULE_SRC_PATH, MODULE_TEST_PATH, MODULE_DEBUG_PATH, \
    MODULE_TEST_FIXTURES_PATH


@pytest.fixture()
def simple_workspace_tree(simple_changelist_xml):
    return workspace.load_xml(simple_changelist_xml)


@pytest.fixture()
def multi_workspace_tree(multi_changelist_xml):
    return workspace.load_xml(multi_changelist_xml)


def create_storage(tree: BaseXMLTree = new_tree()) -> ChangelistDataStorage:
    return wrap_tree_in_storage(tree)


@pytest.fixture()
def simple_storage(simple_changelist_xml: str) -> ChangelistDataStorage:
    return wrap_tree_in_storage(workspace.load_xml(simple_changelist_xml))


@pytest.fixture()
def multi_storage(multi_changelist_xml: str) -> ChangelistDataStorage:
    return wrap_tree_in_storage(workspace.load_xml(multi_changelist_xml))



@pytest.fixture
def shell_scripts_file_pattern() -> SortingFilePattern:
    return SortingFilePattern(file_ext='sh')


@pytest.fixture
def shell_scripts_changelist(shell_scripts_file_pattern: SortingFilePattern) -> SortingChangelist:
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
def sorting_cl_root_markdown_docs() -> SortingChangelist:
    return SortingChangelist(
        module_type=ModuleType.ROOT,
        list_key=compute_key('Documentation'),
        file_patterns=[
            SortingFilePattern(file_ext='md'),
        ],
    )


@pytest.fixture
def sorting_cl_any_markdown_docs() -> SortingChangelist:
    return SortingChangelist(
        module_type=None,
        list_key=compute_key('Documentation'),
        file_patterns=[
            SortingFilePattern(file_ext='md'),
        ],
    )


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


SRC_DIR_PATTERN = SortingFilePattern(first_dir='changelist_sort')
TEST_DIR_PATTERN = SortingFilePattern(first_dir='test')
INPUT_PACKAGE_PATTERN = SortingFilePattern(path_end='input')
SORTING_PACKAGE_PATTERN = SortingFilePattern(path_end='sorting')
WORKSPACE_PACKAGE_PATTERN = SortingFilePattern(path_end='workspace')

BUILD_UPDATES_KEY = list_key.compute_key('Build Updates')


@pytest.fixture
def sorting_cl_input_package_tests() -> SortingChangelist:
    return SortingChangelist(
        list_key.compute_key('Input Package Tests'),
        [
            TEST_DIR_PATTERN,
            INPUT_PACKAGE_PATTERN,
        ],
        ModuleType.MODULE,
    )


@pytest.fixture
def sorting_cl_input_package() -> SortingChangelist:
    return SortingChangelist(
        list_key.compute_key('Input Package'),
        [
            SRC_DIR_PATTERN,
            INPUT_PACKAGE_PATTERN,
        ],
        ModuleType.MODULE,
    )


@pytest.fixture
def sorting_cl_all_files_in_tests() -> SortingChangelist:
    """ All Files in the 'test' Directory.
    """
    return SortingChangelist(
        list_key.compute_key('Tests'),
        [
            TEST_DIR_PATTERN,
        ],
        ModuleType.MODULE,
    )


@pytest.fixture
def sorting_cl_pytest_files() -> SortingChangelist:
    """ Pytest Files: 'test_*.py' files in the 'test' Directory.
    """
    return SortingChangelist(
        list_key.compute_key('Pytest Modules'),
        [
            TEST_DIR_PATTERN,
            SortingFilePattern(filename_prefix='test_'),
            SortingFilePattern(file_ext='py'),
        ],
        ModuleType.MODULE,
    )


@pytest.fixture
def sorting_cl_src_package() -> SortingChangelist:
    """ """
    return SortingChangelist(
        list_key.compute_key('Main Package Source'),
        [
            SRC_DIR_PATTERN,
        ],
        ModuleType.MODULE,
    )


@pytest.fixture
def sort_config_developer_cl_0(
    sorting_cl_input_package_tests,
    sorting_cl_input_package,
    sorting_cl_any_markdown_docs,
    sorting_cl_all_files_in_tests,
    sorting_cl_src_package,
    shell_scripts_changelist,
) -> tuple[SortingChangelist, ...]:
    return (
        sorting_cl_any_markdown_docs,
        sorting_cl_input_package,
        sorting_cl_input_package_tests,
        SortingChangelist(
            list_key.compute_key('Sorting Package Tests'),
            [
                TEST_DIR_PATTERN,
                SORTING_PACKAGE_PATTERN,
            ],
            ModuleType.MODULE,
        ),
        SortingChangelist(
            list_key.compute_key('Workspace Package Tests'),
            [
                TEST_DIR_PATTERN,
                WORKSPACE_PACKAGE_PATTERN,
            ],
            ModuleType.MODULE,
        ),
        sorting_cl_all_files_in_tests,  # Tests that don't match a pattern
        SortingChangelist(
            list_key.compute_key('Sorting Package'),
            [
                SRC_DIR_PATTERN,
                SORTING_PACKAGE_PATTERN,
            ],
            ModuleType.MODULE,
        ),
        SortingChangelist(
            list_key.compute_key('Workspace Package'),
            [
                SRC_DIR_PATTERN,
                WORKSPACE_PACKAGE_PATTERN,
            ],
            ModuleType.MODULE,
        ),
        sorting_cl_src_package,
        shell_scripts_changelist,
        SortingChangelist(
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
            ],
            ModuleType.ROOT,
        ),
        SortingChangelist(
            BUILD_UPDATES_KEY,
            [
                SortingFilePattern(
                    inverse=True,
                    first_dir='gradle',
                ),
                SortingFilePattern(
                    inverse=True,
                    first_dir='',
                ),
            ],
            ModuleType.GRADLE,
        ),
        SortingChangelist(
            BUILD_UPDATES_KEY,
            [
                SortingFilePattern(file_ext='gradle'),
            ],
            ModuleType.ROOT,
        ),
        SortingChangelist(
            BUILD_UPDATES_KEY,
            [
                SortingFilePattern(file_ext='properties'),
            ],
            ModuleType.ROOT,
        ),
        SortingChangelist(
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
            ],
            ModuleType.GRADLE,
        )
    )


@pytest.fixture
def no_changelist_xml() -> str:
    """No ChangelistManager Tag Workspace XML"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="AutoImportSettings">
    <option name="autoReloadType" value="NONE" />
  </component>
</project>"""


@pytest.fixture
def invalid_component_xml() -> str:
    """Invalid Workspace XML"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component>
  </component>
  <component name="ChangeListManager">
    <list default="true" id="af84ea1b-1b24-407d-970f-9f3a2835e933" name="Main" comment="Main Files">
      <change beforePath="$PROJECT_DIR$/main.py" beforeDir="false" />
    </list>
  </component>
</project>"""


@pytest.fixture
def get_cl_simple_xml() -> str:
    """Simple Changelists XML"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<changelists>
<list id="9f60fda2f83a47c88" name="Simple" comment="Main Program Files">
  <change beforePath="/main.py" beforeDir="false"  afterPath="/main.py" afterDir="false" />
</list>
</changelists>"""


@pytest.fixture
def get_cl_multi_xml() -> str:
    """Multi Changelists XML"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<changelists>
<list default="true" id="af84ea1b9f3a2835e933" name="Main" comment="Main Program Files">
  <change beforePath="/history.py" beforeDir="false" />
  <change beforePath="/main.py" beforeDir="false" />
</list>
<list id="9f60fda24c8f83a47c88" name="Test" comment="Test Files">
  <change afterPath="/test/test_file.py" afterDir="false" />
</list>
</changelists>"""


@pytest.fixture
def get_cl_gradle_sources_xml() -> str:
    """Gradle Project SourceSet Changelists XML"""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<changelists>
<list default="true" id="af84ea1b9f3a2835e933" name="Main" comment="Main Program Files">
  <change afterPath="{MODULE_SRC_PATH}" afterDir="false" />
  <change afterPath="{MODULE_TEST_PATH}" afterDir="false" />
  <change afterPath="{MODULE_DEBUG_PATH}" afterDir="false" />
  <change afterPath="{MODULE_TEST_FIXTURES_PATH}" afterDir="false" />
</list>
</changelists>"""

@pytest.fixture
def sorting_xml_sample_1():
    return """<?xml version='1.0' encoding='utf-8'?>
<sorting>
    <changelist key="root" name="Project Root Python Files" module="root">
        <files path_end=".py"></files>
    </changelist>
</sorting>"""


@pytest.fixture
def sorting_xml_sample_2():
    return """<?xml version='1.0' encoding='utf-8'?>
<sorting>
    <changelist key="source" name="Source Files">
        <files file_ext=".py" />
    </changelist>
    <changelist key="text" name="Text Files">
        <files file_ext=".txt" />
    </changelist>
    <changelist key="test" name="Tests">
        <files first_dir="test" />
    </changelist>
</sorting>"""


@pytest.fixture
def sorting_xml_sample_3():
    return """<sorting>
    <changelist key="github" name="GitHub Actions CI" module="hidden">
        <files filename_prefix="ci" />
        <files file_ext="yml" />
    </changelist>
    <changelist key="dependabot" name="GitHub Dependabot" module="hidden">
        <files filename_prefix="dependabot" />
    </changelist>
</sorting>"""


@pytest.fixture
def sorting_xml_sample_4():
    return """<sorting>
    <changelist key="app" name="App Module Source Files" module="module">
        <files file_ext="kt" />
    </changelist>
    <changelist key="app" name="App Module Source Files" module="module">
        <files file_ext="java" />
    </changelist>
    <changelist key="gradle" name="Gradle Build Files" module="gradle">
        <files inverse="true" />
    </changelist>
</sorting>"""


@pytest.fixture
def sorting_xml_sample_4_no_cl_name_attrs():
    return """<sorting>
    <changelist key="App Module Source Files" module="module">
        <files file_ext="kt" />
    </changelist>
    <changelist key="App Module Source Files" module="module">
        <files file_ext="java" />
    </changelist>
    <changelist key="Gradle Build Files" module="gradle">
        <files inverse="true" />
    </changelist>
</sorting>"""


@pytest.fixture
def sorting_config_list_sample1():
    return [
        SortingChangelist(
            list_key=ListKey('root', 'Project Root Python Files'),
            file_patterns=[
                SortingFilePattern(
                    path_end='.py',
                ),
            ],
            module_type=ModuleType.ROOT,
        ),
    ]


@pytest.fixture
def sorting_config_list_sample2():
    return [
        SortingChangelist(
            list_key=ListKey('source', 'Source Files'),
            file_patterns=[
                SortingFilePattern(file_ext='.py')
            ],
        ),
        SortingChangelist(
            list_key=ListKey('text', 'Text Files'),
            file_patterns=[
                SortingFilePattern(file_ext='.txt')
            ],
        ),
        SortingChangelist(
            list_key=ListKey('test', 'Tests'),
            file_patterns=[
                SortingFilePattern(first_dir='test')
            ],
        ),
    ]


@pytest.fixture
def sorting_config_list_sample3():
    return [
        SortingChangelist(
            list_key=ListKey("github", "GitHub Actions CI"),
            file_patterns=[
                SortingFilePattern(filename_prefix='ci'),
                SortingFilePattern(file_ext='yml'),
            ],
            module_type=ModuleType.HIDDEN,
        ),
        SortingChangelist(
            list_key=ListKey("dependabot", "GitHub Dependabot"),
            file_patterns=[
                SortingFilePattern(filename_prefix='dependabot'),
            ],
            module_type=ModuleType.HIDDEN,
        ),
    ]


@pytest.fixture
def sorting_config_list_sample4():
    return [
        SortingChangelist(
            list_key=ListKey("app", "App Module Source Files"),
            file_patterns=[
                SortingFilePattern(file_ext='kt'),
            ],
            module_type=ModuleType.MODULE,
        ),
        SortingChangelist(
            list_key=ListKey("app", "App Module Source Files"),
            file_patterns=[
                SortingFilePattern(file_ext='java'),
            ],
            module_type=ModuleType.MODULE,
        ),
        SortingChangelist(
            list_key=ListKey("gradle", "Gradle Build Files"),
            file_patterns=[
                SortingFilePattern(inverse=True),
            ],
            module_type=ModuleType.GRADLE,
        ),
    ]

@pytest.fixture
def sorting_config_list_sample4_no_cl_name_attrs():
    return [
        SortingChangelist(
            list_key=ListKey("appmodulesourcefiles", "App Module Source Files"),
            file_patterns=[
                SortingFilePattern(file_ext='kt'),
            ],
            module_type=ModuleType.MODULE,
        ),
        SortingChangelist(
            list_key=ListKey("appmodulesourcefiles", "App Module Source Files"),
            file_patterns=[
                SortingFilePattern(file_ext='java'),
            ],
            module_type=ModuleType.MODULE,
        ),
        SortingChangelist(
            list_key=ListKey("gradlebuildfiles", "Gradle Build Files"),
            file_patterns=[
                SortingFilePattern(inverse=True),
            ],
            module_type=ModuleType.GRADLE,
        ),
    ]