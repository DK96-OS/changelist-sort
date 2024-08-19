"""Testing Argument Parser Methods.
"""
from changelist_sort.input.argument_parser import parse_arguments


def test_parse_arguments_empty_list():
    result = parse_arguments()
    assert result.workspace_path is None


def test_parse_arguments_empty_list():
    result = parse_arguments('')
    assert result.workspace_path is None


def test_parse_arguments_change_list_main_empty_workspace_arg():
    try:
        result = parse_arguments(['--workspace', ''])
        assert False
    except SystemExit:
        assert True


def test_parse_arguments_change_list_main():
    result = parse_arguments(['--workspace', 'workspace.xml'])
    assert result.workspace_path == 'workspace.xml'
