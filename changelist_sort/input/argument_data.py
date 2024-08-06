"""The Arguments Received from the Command Line Input.

This DataClass is created after the argument syntax is validated.

Syntax Validation:
-
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ArgumentData:
    """
    The syntactically valid arguments recevied by the Program.

    Fields:
    - workspace_path (str): The path to the workspace file.
    """
    workspace_path: str | None
