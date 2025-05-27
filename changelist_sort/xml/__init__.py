""" Sort XML.
"""
from pathlib import Path
from typing import Generator

from changelist_data.storage import file_validation

from changelist_sort.sorting.sorting_changelist import SortingChangelist
from changelist_sort.xml import reader


# These are the relative paths that are checked for sorting configuration
SORT_XML_LOCATIONS = (
    ".changelists/sort.xml",
    ".changelists/sorting.xml",
#    ".changelist/sort.xml",
#    "changelists/sort.xml",
#    "changelist/sort.xml",
)


def _ensure_sort_xml_file_exists(
    sort_xml_path: Path | None,
    overwrite: bool = False,
) -> Path | None:
    """ Find a sort_xml file path.
- If no path is provided and no default file is found, creates it in the first default location.

**Parameters**:
 - sort_xml_path (Path?): The path to the SortXML file, if not default. If None, searches the Default Locations.
 - overwrite (bool): Whether to overwrite existing files containing more than 8 bytes.

**Returns:**
 Path? - The path to the file, whether it already exists, or has just been created.
    """
    if sort_xml_path is not None:
        if file_validation.file_exists(sort_xml_path):
            if sort_xml_path.stat().st_size > 8 and not overwrite:
                return None # The file exists, but don't overwrite it.
            return sort_xml_path
        # Create the File where the argument specified
        output_file = sort_xml_path
    else: # Search all potential locations
        for potential_path in SORT_XML_LOCATIONS:
            if file_validation.file_exists(output_file := Path(potential_path)):
                return output_file # Found file in a default location
        # Create the File in the Default Location
        output_file = Path(SORT_XML_LOCATIONS[0])
    output_file.parent.mkdir(exist_ok=True)
    output_file.touch(exist_ok=True)
    return output_file


def load_sorting_config(
    sort_xml_path: Path | None = None,
) -> list[SortingChangelist] | None:
    """ Search for the Sorting Config file and load it.
 - If file exists, but fails to parse, then exit.

**Parameters:**
 - sort_xml_path (Path?): A Path to the Sorting Config. If None, searches the SortXMLLocations tuple in order.

**Returns:**
 list[SortingChangelist]? - The list of SortingChangelist data objects created from the SortXML file.
    """
    return list(generate_sorting_config(sort_xml_path))


def generate_sorting_config(
    sort_xml_path: Path | None = None,
) -> Generator[SortingChangelist, None, None]:
    """ Search for the Sorting Config file and load it.
 - If file exists, but fails to parse, then exit.

**Parameters:**
 - sort_xml_path (Path?): The Path to the SortXML File. If None, searches SortXMLLocation tuple in order.

**Yields:**
 SortingChangelist - The SortingChangelist data objects created from the SortXML file.
        """
    if (result := _argument_logic(sort_xml_path)) is None:
        exit("No Sorting Config File Exists. Create one with --generate_sort_xml")
    yield from reader.generate_sort_config_from_xml(result)


def _argument_logic(
    sort_xml_path: Path | None,
) -> str | None:
    if sort_xml_path is not None:
        if file_validation.file_exists(f := Path(sort_xml_path)):
            return _read_file(f)
        exit(f"Sort XML file does not exist: {sort_xml_path}")
    for file_path_str in SORT_XML_LOCATIONS:
        if file_validation.file_exists(f := Path(file_path_str)):
            return _read_file(f)
    return None


def _read_file(file_path: Path) -> str:
    try:
        return file_path.read_text()
    except SystemExit as e:
        exit(f"Error Occurred while reading Sort XML file: {e}")