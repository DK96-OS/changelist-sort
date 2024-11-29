""" XML Sort Config Reader Methods.
"""
from xml.etree.ElementTree import fromstring, Element, ParseError

from changelist_sort import list_key
from changelist_sort.list_key import ListKey
from changelist_sort.sorting.sorting_changelist import SortingChangelist
from changelist_sort.sorting.sorting_file_pattern import SortingFilePattern
from changelist_sort.sorting.module_type import ModuleType
from changelist_data.xml import xml_reader


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
    for elem in xml_reader.filter_by_tag(xml_root, 'sorting'):
        return elem
    return None


def extract_sorting_config(changelists_element: Element) -> list[SortingChangelist]:
    """ Given the Changelist Manager Element, obtain the list of List Elements.

    Parameters:
    - changelist_manager (Element): The ChangeList Manager XML Element.

    Returns:
    list[Element] - A List containing the Lists.
    """
    return [
        SortingChangelist(
            module_type=_determine_module_type(
                xml_reader.get_attr(cl_element, 'module_type')
            ),
            list_key=_extract_changelist_key(cl_element),
            file_patterns=_extract_file_pattern(cl_element),
        ) for cl_element in xml_reader.filter_by_tag(changelists_element, 'changelist')
    ]


def _extract_changelist_key(cl_element: Element) -> ListKey:
    """ Extract the List Key attributes from the Element.
    """
    key = xml_reader.get_attr_or(cl_element, 'list_key', 'default')
    if (name := xml_reader.get_attr(cl_element, 'list_name')) is None:
        return list_key.compute_key(key)
    return ListKey(key=key, changelist_name=name)


def _extract_file_pattern(
    changelist_element: Element,
) -> list[SortingFilePattern]:
    """ Given a File Pattern XML Element, obtain the List of Changes.

    Parameters:
    - changelist_element (Element): The Element representing a Changelist.

    Returns:
    list[DeveloperFilePattern] - The list of FilePattern.
    """
    return [
        SortingFilePattern(
            file_ext=xml_reader.get_attr(file_pattern, 'file_ext'),
            first_dir=xml_reader.get_attr(file_pattern, 'first_dir'),
            filename_prefix=xml_reader.get_attr(file_pattern, 'filename_prefix'),
            filename_suffix=xml_reader.get_attr(file_pattern, 'filename_suffix'),
            path_start=xml_reader.get_attr(file_pattern, 'path_start'),
            path_end=xml_reader.get_attr(file_pattern, 'path_end'),
        ) for file_pattern in xml_reader.filter_by_tag(changelist_element, 'files')
    ]


def _determine_module_type(module_type: str) -> ModuleType | None:
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
