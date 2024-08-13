""" File Paths used as examples in Tests.
"""
from changelist_sort.change_data import ChangeData
from changelist_sort.changelist_data import ChangelistData


MODULE_SRC_PATH = '/module/src/main/java/module/Main.java'
MODULE_TEST_PATH = '/module/src/test/java/module/MainTest.java'
ROOT_GRADLE_PATH = '/build.gradle'
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
