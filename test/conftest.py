"""
"""
from pathlib import Path

import pytest
from changelist_data.storage import ChangelistDataStorage, StorageType
from changelist_data.xml.base_xml_tree import BaseXMLTree

from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_data import ChangelistData
from changelist_sort.sorting import module_sort

MODULE_SRC_PATH = '/module/src/main/java/module/Main.java'
MODULE_TEST_PATH = '/module/src/test/java/module/MainTest.java'
MODULE_DEBUG_PATH = '/module/src/debug/java/module/MainDebug.java'
ROOT_GRADLE_PATH = '/build.gradle'
ROOT_README_PATH = '/README.md'
GRADLE_PROPERTIES_PATH = '/gradle/wrapper/gradle-wrapper.properties'
APP_GRADLE_PATH = '/app/build.gradle'
GITHUB_WORKFLOW_PATH = '/.github/workflows/build_and_test.yml'
GITHUB_DEPENDABOT_PATH = '/.github/dependabot.yml'

PYTHON_READER_PATH = '/changelist_sort/xml/sort_xml_reader.py'
PYTHON_TEST_PATH = '/test/changelist_sort/xml/test_sort_xml_reader.py'


def get_change_data(after_path: str) -> ChangeData:
    return ChangeData(
        after_path=after_path,
        after_dir=False,
    )


@pytest.fixture
def module_src_change_data() -> ChangeData:
    return get_change_data(MODULE_SRC_PATH)


@pytest.fixture
def module_test_change_data() -> ChangeData:
    return get_change_data(MODULE_TEST_PATH)


@pytest.fixture
def module_debug_change_data() -> ChangeData:
    return get_change_data(MODULE_DEBUG_PATH)


@pytest.fixture
def root_gradle_build_change_data() -> ChangeData:
    return get_change_data(ROOT_GRADLE_PATH)


@pytest.fixture
def root_readme_change_data() -> ChangeData:
    return get_change_data(ROOT_README_PATH)


@pytest.fixture
def gradle_properties_change_data() -> ChangeData:
    return get_change_data(GRADLE_PROPERTIES_PATH)


@pytest.fixture
def app_gradle_build_change_data() -> ChangeData:
    return get_change_data(APP_GRADLE_PATH)


@pytest.fixture
def github_workflows_change_data() -> ChangeData:
    return get_change_data(GITHUB_WORKFLOW_PATH)


@pytest.fixture
def dependabot_change_data() -> ChangeData:
    return get_change_data(GITHUB_DEPENDABOT_PATH)


@pytest.fixture
def python_reader_cd() -> ChangeData:
    return get_change_data(PYTHON_READER_PATH)


@pytest.fixture
def python_test_cd() -> ChangeData:
    return get_change_data(PYTHON_TEST_PATH)


@pytest.fixture
def module_changelist() -> ChangelistData:
    """ Creates a Changelist called Module.
    """
    return ChangelistData(
        id='231341512',
        name='Module',
        changes=[],
    )


@pytest.fixture
def app_changelist() -> ChangelistData:
    """ Creates a Changelist called App.
        Default Changes are empty.
    """
    return ChangelistData(
        id='1234',
        name='App',
        changes=[],
    )


@pytest.fixture
def build_updates_changelist(root_gradle_build_change_data) -> ChangelistData:
    return ChangelistData(
        id='1234563',
        name='Build Updates',
        changes=[root_gradle_build_change_data],
    )


@pytest.fixture
def github_changelist() -> ChangelistData:
    return ChangelistData(
        id='1234563',
        name='GitHub',
        changes=[],
    )


@pytest.fixture
def github_workflows_changelist() -> ChangelistData:
    return ChangelistData(
        id='123456331',
        name='GitHub Workflows',
        changes=[],
    )


@pytest.fixture
def root_changelist() -> ChangelistData:
    return ChangelistData(
        id='1234509',
        name='Root',
        changes=[],
    )


@pytest.fixture
def multiple_gradle_changelists():
    """
    Create a list of Changelists from the DeveloperChangelists Gradle Module CLs.
    """
    return [
        ChangelistData(
            id=str(1) + name.key,
            name=name.changelist_name,
        ) for name in module_sort.MODULE_GRADLE_CL_TUPLE
    ]


def wrap_tree_in_storage(tree: BaseXMLTree) -> ChangelistDataStorage:
    return ChangelistDataStorage(tree, StorageType.CHANGELISTS, Path('testfile'))


@pytest.fixture
def simple_changelist_xml() -> str:
    """Simple Workspace XML"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="AutoImportSettings">
    <option name="autoReloadType" value="NONE" />
  </component>
  <component name="ChangeListManager">
    <list id="9f60fda2-421e-4a4b-bd0f-4c8f83a47c88" name="Simple" comment="Main Program Files">
      <change beforePath="$PROJECT_DIR$/main.py" beforeDir="false"  afterPath="$PROJECT_DIR$/main.py" afterDir="false" />
    </list>
  </component>
</project>"""


@pytest.fixture
def multi_changelist_xml() -> str:
    """Simple Workspace XML"""
    return """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="AutoImportSettings">
    <option name="autoReloadType" value="NONE" />
  </component>
  <component name="ChangeListManager">
    <list default="true" id="af84ea1b-1b24-407d-970f-9f3a2835e933" name="Main" comment="Main Program Files">
      <change beforePath="$PROJECT_DIR$/history.py" beforeDir="false" />
      <change beforePath="$PROJECT_DIR$/main.py" beforeDir="false" />
    </list>
    <list id="9f60fda2-421e-4a4b-bd0f-4c8f83a47c88" name="Test" comment="Test Files">
      <change afterPath="$PROJECT_DIR$/test/test_file.py" afterDir="false" />
    </list>
  </component>
</project>"""


@pytest.fixture
def temp_cwd():
    """ Creates a Temporary Working Directory for Git subprocesses.
    """
    from tempfile import TemporaryDirectory
    tdir = TemporaryDirectory()
    from os import getcwd, chdir
    initial_cwd = getcwd()
    chdir(tdir.name)
    yield tdir
    chdir(initial_cwd)
    tdir.cleanup()


def get_temp_changelist_dir_absolute_path(temp_cwd):
    (temp_cl_dir := (Path(temp_cwd.name) / '.changelists')).mkdir()
    return temp_cl_dir.absolute()