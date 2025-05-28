""" Testing Package-Level Method: read_xml, generate_sort_config_from_xml
 - Note: read_xml calls generate_sort_config_from_xml method, wraps it in a list.
"""
import pytest

from changelist_sort.xml import reader
from changelist_sort.xml.reader import read_xml


def test_read_xml_empty_returns_none():
    assert read_xml('') is None


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


def test_sample4(
    sorting_xml_sample_4,
    sorting_config_list_sample4,
):
    assert read_xml(sorting_xml_sample_4) == sorting_config_list_sample4


def test_sample4_no_cl_name_attrs(
    sorting_xml_sample_4_no_cl_name_attrs,
    sorting_config_list_sample4_no_cl_name_attrs,
):
    assert read_xml(sorting_xml_sample_4_no_cl_name_attrs) == sorting_config_list_sample4_no_cl_name_attrs


def test_read_xml_invalid_raises_exit():
    with pytest.raises(SystemExit):
        read_xml('<some_bad_xml>')


def test_determine_module_type_non_supported_inputs_returns_none():
    assert reader._determine_module_type('abc') is None