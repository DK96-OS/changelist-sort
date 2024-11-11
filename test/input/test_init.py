""" Testing Input Package Init Module Methods.
"""
from pathlib import Path

import changelist_data
import pytest
from changelist_data.storage import ChangelistDataStorage
from changelist_data.xml.changelists import new_tree

from changelist_sort.input import validate_input
from changelist_sort.sorting.sort_mode import SortMode
from test import data_provider
from test.changelist_sort.workspace.test_workspace_tree import multi_workspace_tree


def create_storage() -> ChangelistDataStorage:
    return new_tree()


@pytest.fixture(autouse=True)
def test_validate_input_no_args_ws_file_does_not_exist_raises_exit(monkeypatch):
    test_input = []
    monkeypatch.setattr(Path, 'exists', lambda _: False)
    try:
        validate_input(test_input)
        assert False
    except SystemExit:
        assert True


@pytest.fixture(autouse=True)
def test_validate_input_no_args_ws_file_is_empty_raises_exit(monkeypatch):
    test_input = []
    monkeypatch.setattr(Path, 'exists', lambda _: True)
    monkeypatch.setattr(Path, 'read_text', lambda _: '')
    try:
        validate_input(test_input)
        assert False
    except SystemExit:
        assert True


@pytest.fixture(autouse=True)
def test_validate_input_no_args_ws_file_has_no_cl_(monkeypatch):
    test_input = []
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'is_file', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        result = validate_input(test_input)
    assert len(result.storage.get_changelists()) == 0


def test_validate_input_no_args_ws_file_simple_cl_(simple_workspace_tree):
    test_input = []
    def storage_expects(storage_type, path):
        if storage_type is not None:
            exit("Provided Storage Type was None")
        if path is not None:
            exit("Provided Path was None")
        return simple_workspace_tree
    with pytest.MonkeyPatch().context() as c:
        c.setattr(changelist_data.storage, 'load_storage', storage_expects)
        result = validate_input(test_input)
    assert len(result.storage.get_changelists()) == 1


def test_validate_input_no_args_ws_file_multi_cl_(multi_workspace_tree):
    test_input = []
    def storage_expects(storage_type, path):
        if storage_type is not None:
            exit("Provided Storage Type was None")
        if path is not None:
            exit("Provided Path was None")
        return multi_workspace_tree
    with pytest.MonkeyPatch().context() as c:
        c.setattr(changelist_data.storage, 'load_storage', storage_expects)
        result = validate_input(test_input)
        assert len(result.storage.get_changelists()) == 1



def test_validate_input_ws_path_arg_is_empty_raises_exit():
    test_input = ['--workspace', '']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        try:
            validate_input(test_input)
            assert False
        except SystemExit:
            assert True


def test_validate_input_ws_path_arg_is_missing_raises_exit():
    test_input = ['--workspace']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        try:
            validate_input(test_input)
            assert False
        except SystemExit:
            assert True


def test_validate_input_ws_path_arg_does_not_exist_raises_exit():
    test_input = ['--workspace', '/file.xml']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: False)
        try:
            validate_input(test_input)
            assert False
        except SystemExit:
            assert True


def test_validate_input_developer_sort():
    test_input = ['-d']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        result = validate_input(test_input)
        assert result.workspace_path == Path('.idea/workspace.xml')
        assert result.sort_mode == SortMode.DEVELOPER


def test_validate_input_sourceset_sort():
    test_input = ['-s']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        result = validate_input(test_input)
        assert result.workspace_path == Path('.idea/workspace.xml')
        assert result.sort_mode == SortMode.SOURCESET


def test_validate_input_remove_empty():
    test_input = ['-r']
    with pytest.MonkeyPatch().context() as c:
        c.setattr(Path, 'exists', lambda _: True)
        c.setattr(Path, 'read_text', lambda _: data_provider.get_no_changelist_xml())
        result = validate_input(test_input)
        assert result.workspace_path == Path('.idea/workspace.xml')
        assert result.sort_mode == SortMode.MODULE
        assert result.remove_empty
