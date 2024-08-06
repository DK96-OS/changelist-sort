"""The Input Package for Changelist Sort
"""
from pathlib import Path

from changelist_sort.input.argument_data import ArgumentData
from changelist_sort.input.argument_parser import parse_arguments
from changelist_sort.input.file_validation import validate_input_file
from changelist_sort.input.input_data import InputData


def validate_input(args_list: list[str]) -> InputData:
    """
    Validate the Argument Data into InputData.
    """
    arg_data = parse_arguments(args_list)
    ws_path = _find_workspace_file(arg_data)
    return InputData(
        workspace_xml=validate_input_file(ws_path),
        workspace_path=ws_path
    )


def _find_workspace_file(arg_data: ArgumentData) -> Path:
    if arg_data.workspace_path is None:
        current_dir = Path('.')
        return current_dir / '.idea' / 'workspace.xml'
    else:
        return arg_data.workspace_path
