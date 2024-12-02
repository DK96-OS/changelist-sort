""" Reads the contents of a Sort XML file.
"""
from changelist_sort.sorting.sorting_changelist import SortingChangelist
from changelist_sort.xml.sort_xml_reader import parse_xml, read_sorting_element, find_sorting_root


def read_xml(sorting_xml: str) -> list[SortingChangelist]:
    """ Parse the Sorting XML file and obtain all Developer Changelist data in a list.
    """
    if (sorting_root := find_sorting_root(parse_xml(sorting_xml))) is not None:
        return read_sorting_element(sorting_root)
