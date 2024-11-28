""" Testing Package-Level Method: read_xml.
"""
from changelist_sort.xml import read_xml


def test_sample1(
    sorting_xml_sample_1,
    sorting_config_list_sample1,
):
    assert read_xml(sorting_xml_sample_1) == sorting_config_list_sample1


def test_sample2(
    sorting_xml_sample_2,
    sorting_config_list_sample2,
):
    assert read_xml(sorting_xml_sample_2) == sorting_config_list_sample2


def test_sample3(
    sorting_xml_sample_3,
    sorting_config_list_sample3,
):
    assert read_xml(sorting_xml_sample_3) == sorting_config_list_sample3
