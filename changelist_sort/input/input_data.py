"""Valid Input Data Class.
"""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InputData:
    """A Data Class Containing Program Input.

    Fields:
    - workspace_xml (str): The contents of the Workspace XML file.
    - workspace_path (Path): The Path to the Workspace File.
    """
    workspace_xml: str
    workspace_path: Path
