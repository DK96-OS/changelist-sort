""" XML Sort Definitions, Parsing and Reading Methods.
"""
from xml.etree.ElementTree import fromstring, Element, ParseError

from changelist_sort import list_key
from changelist_sort.list_key import ListKey
from changelist_sort.sorting.sorting_changelist import SortingChangelist
from changelist_sort.sorting.sorting_file_pattern import SortingFilePattern
from changelist_sort.sorting.module_type import ModuleType
from changelist_data.xml import xml_reader


# These are the XML Tags used in the Sort.XML file
ROOT_TAG = "sorting"
CHANGELIST_TAG = "changelist"
CHANGELIST_KEY = "key"
CHANGELIST_NAME = "name"
CHANGELIST_MODULE = "module"
CHANGELIST_DEFAULT = "is_default"
# Files are nested elements within a changelist
FILES_TAG = "files"
FILES_PATH_START = "path_start"
FILES_PATH_END = "path_end"
FILES_FILENAME_PREFIX = "filename_prefix"
FILES_FILENAME_SUFFIX = "filename_suffix"
FILES_EXTENSION = "file_ext"
FILES_FIRST_DIR = "first_dir"


def parse_xml(sorting_xml: str) -> Element:
    """ Parse an XML file. This should be a Sorting XML file.

    Parameters:
    - sorting_xml (str): The Sorting data in xml format.

    Returns:
    Element - the XML Root Element

    Raises:
    SystemExit - if the xml could not be parsed.
    """
    try:
        return fromstring(sorting_xml)
    except ParseError:
        exit("Unable to Parse Sorting XML File.")


def find_sorting_root(xml_root: Element) -> Element | None:
    """ Extract the Sorting Root XML Element.
    """
    for elem in xml_reader.filter_by_tag(xml_root, ROOT_TAG):
        return elem
    return None


def read_sorting_element(sorting_element: Element) -> list[SortingChangelist]:
    """ Given the Changelist Manager Element, obtain the list of List Elements.

    Parameters:
    - changelist_manager (Element): The ChangeList Manager XML Element.

    Returns:
    list[Element] - A List containing the Lists.
    """
    return [
        SortingChangelist(
            module_type=_determine_module_type(
                xml_reader.get_attr(cl_element, CHANGELIST_MODULE)
            ),
            list_key=_read_changelist_key(cl_element),
            file_patterns=_read_file_patterns(cl_element),
        ) for cl_element in xml_reader.filter_by_tag(sorting_element, CHANGELIST_TAG)
    ]


def _read_changelist_key(cl_element: Element) -> ListKey:
    """ Extract the ListKey from the Changelist Element.
        - Checks if Changelist Name is present, as ListKey contains both name and key.
        - If no Name attribute is present, the ListKey generates a name from the key.
    """
    key = xml_reader.get_attr_or(cl_element, CHANGELIST_KEY, 'default')
    if (name := xml_reader.get_attr(cl_element, CHANGELIST_NAME)) is None:
        return list_key.compute_key(key)
    return ListKey(key=key, changelist_name=name)


def _read_file_patterns(
    changelist_element: Element,
) -> list[SortingFilePattern]:
    """ Given a File Pattern XML Element, obtain the List of Changes.
        - Searches for all potential file pattern attributes.
        - Returns all found in a SortingFilePattern dataclass object.

    Parameters:
    - changelist_element (Element): The XML Element representing a Changelist.

    Returns:
    list[DeveloperFilePattern] - The list of FilePattern objects for the Changelist.
    """
    return [
        _create_file_pattern(changelist_element, file_pattern)
        for file_pattern in xml_reader.filter_by_tag(changelist_element, FILES_TAG)
    ]


def _create_file_pattern(cl_element: Element, file_pattern: Element) -> SortingFilePattern:
    """"""
    try:
        return SortingFilePattern(
            file_ext=xml_reader.get_attr(file_pattern, FILES_EXTENSION),
            first_dir=xml_reader.get_attr(file_pattern, FILES_FIRST_DIR),
            filename_prefix=xml_reader.get_attr(file_pattern, FILES_FILENAME_PREFIX),
            filename_suffix=xml_reader.get_attr(file_pattern, FILES_FILENAME_SUFFIX),
            path_start=xml_reader.get_attr(file_pattern, FILES_PATH_START),
            path_end=xml_reader.get_attr(file_pattern, FILES_PATH_END),
        )
    except SystemExit:
        exit(f"Found FilePattern Error in Changelist with Key:{_read_changelist_key(cl_element)}")


def _determine_module_type(module_type: str | None) -> ModuleType | None:
    """ Determine the ModuleType, or return None.
    """
    if module_type is None or not isinstance(module_type, str):
        return None
    elif (m := module_type.lower()) == 'module':
        return ModuleType.MODULE
    elif m == 'root':
        return ModuleType.ROOT
    elif m == 'gradle':
        return ModuleType.GRADLE
    elif m == 'hidden':
        return ModuleType.HIDDEN
    else:
        return None