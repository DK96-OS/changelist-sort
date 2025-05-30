""" Testing Argument Parser Methods.
"""
import pytest

from changelist_sort.input.argument_parser import parse_arguments


def test_parse_arguments_empty_list_returns_none():
    result = parse_arguments()
    assert result.workspace_path is None


def test_parse_arguments_empty_str_returns_none():
    result = parse_arguments('')
    assert result.workspace_path is None


def test_parse_arguments_too_many_arguments_raises_exit():
    with pytest.raises(SystemExit):
        parse_arguments(list(f"{i}" for i in range(35, 80)))


def test_parse_arguments_invalid_argument_raises_exit():
    with pytest.raises(SystemExit):
        parse_arguments('-a')


def test_parse_arguments_change_list_main_empty_changelist_arg():
    try:
        parse_arguments(['--changelist', ''])
        assert False
    except SystemExit:
        assert True


def test_parse_arguments_change_list_main_empty_workspace_arg():
    try:
        parse_arguments(['--workspace', ''])
        assert False
    except SystemExit:
        assert True


def test_parse_arguments_changelists_cl():
    result = parse_arguments(['--changelists', 'data.xml'])
    assert result.changelists_path == 'data.xml'
    assert result.workspace_path is None
    assert not result.generate_sort_xml


def test_parse_arguments_workspace_cl():
    result = parse_arguments(['--workspace', 'workspace.xml'])
    assert result.changelists_path is None
    assert result.workspace_path == 'workspace.xml'
    assert not result.generate_sort_xml


def test_parse_arguments_sourceset_short_flag():
    result = parse_arguments(['-s'])
    assert result.workspace_path is None
    assert result.sourceset_sort
    assert not result.generate_sort_xml


def test_parse_arguments_sourceset_long():
    result = parse_arguments(['--sourceset-sort'])
    assert result.workspace_path is None
    assert result.sourceset_sort
    assert not result.generate_sort_xml


def test_parse_arguments_sourceset_long2():
    result = parse_arguments(['--sourceset_sort'])
    assert result.workspace_path is None
    assert result.sourceset_sort
    assert not result.generate_sort_xml


def test_parse_arguments_remove_empty_short_flag():
    result = parse_arguments(['-r'])
    assert result.workspace_path is None
    assert not result.sourceset_sort
    assert result.remove_empty
    assert not result.generate_sort_xml


def test_parse_arguments_remove_empty_long():
    result = parse_arguments(['--remove-empty'])
    assert result.workspace_path is None
    assert not result.sourceset_sort
    assert result.remove_empty
    assert not result.generate_sort_xml


def test_parse_arguments_remove_empty_long2():
    result = parse_arguments(['--remove_empty'])
    assert result.workspace_path is None
    assert not result.sourceset_sort
    assert result.remove_empty
    assert not result.generate_sort_xml


def test_parse_arguments_generate_sort_xml():
    result = parse_arguments(['--generate_sort_xml'])
    assert result.changelists_path is None
    assert result.workspace_path is None
    assert not result.sourceset_sort
    assert not result.remove_empty
    assert result.generate_sort_xml