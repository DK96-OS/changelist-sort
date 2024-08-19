""" File Paths used as examples in Tests.
"""
from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_data import ChangelistData
from changelist_sort.sorting import module_sort


MODULE_SRC_PATH = '/module/src/main/java/module/Main.java'
MODULE_TEST_PATH = '/module/src/test/java/module/MainTest.java'
ROOT_GRADLE_PATH = '/build.gradle'
ROOT_README_PATH = '/README.md'
GRADLE_PROPERTIES_PATH = '/gradle/wrapper/gradle-wrapper.properties'
APP_GRADLE_PATH = '/app/build.gradle'
GITHUB_WORKFLOW_PATH = '/.github/workflows/build_and_test.yml'
GITHUB_DEPENDABOT_PATH = '/.github/dependabot.yml'


def get_change_data(after_path: str) -> ChangeData:
    return ChangeData(
        after_path=after_path,
        after_dir=False,
    )


def get_module_src_change_data() -> ChangeData:
    return get_change_data(MODULE_SRC_PATH)


def get_module_test_change_data() -> ChangeData:
    return get_change_data(MODULE_TEST_PATH)


def get_root_gradle_build_change_data() -> ChangeData:
    return get_change_data(ROOT_GRADLE_PATH)


def get_root_readme_change_data() -> ChangeData:
    return get_change_data(ROOT_README_PATH)


def get_gradle_properties_change_data() -> ChangeData:
    return get_change_data(GRADLE_PROPERTIES_PATH)


def get_app_gradle_build_change_data() -> ChangeData:
    return get_change_data(APP_GRADLE_PATH)


def get_github_workflows_change_data() -> ChangeData:
    return get_change_data(GITHUB_WORKFLOW_PATH)


def get_github_dependabot_change_data() -> ChangeData:
    return get_change_data(GITHUB_DEPENDABOT_PATH)


def get_module_changelist(
    changes: list[ChangeData] = [get_module_src_change_data(), get_module_test_change_data()],
) -> ChangelistData:
    """
    Creates a Changelist called Module.
        Default Changes include a src and a test file.
    """
    return ChangelistData(
        id='231341512',
        name='Module',
        changes=changes,
    )


def get_app_changelist(
    changes: list[ChangeData] = [],
) -> ChangelistData:
    """
    Creates a Changelist called App.
        Default Changes are empty.
    """
    return ChangelistData(
        id='1234',
        name='App',
        changes=changes,
    )


def get_build_updates_changelist(
    changes: list[ChangeData] = [get_root_gradle_build_change_data()],
) -> ChangelistData:
    return ChangelistData(
        id='1234563',
        name='Build Updates',
        changes=changes,
    )


def get_github_changelist(
    changes: list[ChangeData] = [],
) -> ChangelistData:
    return ChangelistData(
        id='1234563',
        name='GitHub',
        changes=changes,
    )


def get_root_changelist(
    changes: list[ChangeData] = [],
) -> ChangelistData:
    return ChangelistData(
        id='1234509',
        name='Root',
        changes=changes,
    )


def get_multiple_gradle_changelists():
    """
    Create a list of Changelists from the DeveloperChangelists Gradle Module CLs.
    """
    return [ 
        ChangelistData(
            id=str(1) + name.key,
            name=name.changelist_name,
        ) for name in module_sort.MODULE_GRADLE_CL_TUPLE
    ]


def get_no_changelist_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="AutoImportSettings">
    <option name="autoReloadType" value="NONE" />
  </component>
</project>"""


def get_simple_changelist_xml() -> str:
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


def get_multi_changelist_xml() -> str:
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


def get_invalid_component_xml() -> str:
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
