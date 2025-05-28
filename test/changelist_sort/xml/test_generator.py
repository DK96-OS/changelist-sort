""" Testing the Sort XML Generator Module.
"""
import pytest

from changelist_sort.xml import generator, reader, _ensure_sort_xml_file_exists
from test.conftest import get_temp_changelist_dir_absolute_path

INITIAL_ELEMENT_TREE = generator.create_initial_sort_xml_tree()
_ROOT_ELEMENT = INITIAL_ELEMENT_TREE.getroot()


def test_initial_element_tree_root_tag():
    assert _ROOT_ELEMENT.tag == reader.ROOT_TAG


def test_initial_element_tree_changelists():
    result = list(_ROOT_ELEMENT.iterfind('changelist'))
    assert len(result) == 3
    assert result[0].get('name') == 'Project Root'
    assert result[1].get('name') == 'Tests'
    assert result[2].get('name') == 'Changelists Config'


def test_ensure_sort_xml_file_exists_empty_cwd_returns_new_empty_file_path(temp_cwd):
    result = _ensure_sort_xml_file_exists(None)
    assert '' == result.absolute().read_text()


def test_ensure_sort_xml_file_exists_empty_sort_xml_exists_returns_empty_file_path(temp_cwd):
    temp_cl_dir = get_temp_changelist_dir_absolute_path(temp_cwd)
    (temp_sort_xml := (temp_cl_dir / 'sort.xml')).touch()
    # The file is empty,
    assert temp_sort_xml == _ensure_sort_xml_file_exists(None).absolute()


def test_ensure_sort_xml_file_exists_contains_message_returns_path(temp_cwd):
    temp_cl_dir = get_temp_changelist_dir_absolute_path(temp_cwd)
    (temp_sort_xml := (temp_cl_dir / 'sort.xml')).touch()
    temp_sort_xml.write_text('Hello Reader!')
    # The file contains something.
    assert temp_sort_xml == _ensure_sort_xml_file_exists(None).absolute()


def test_generate_sort_xml_invalid_argument_type_raises_type_error():
    with pytest.raises(TypeError):
        generator.generate_sort_xml(4)


def test_generate_sort_xml_none_file_exists_empty_sort_xml_exists_returns_true(temp_cwd):
    temp_cl_dir = get_temp_changelist_dir_absolute_path(temp_cwd)
    (temp_sort_xml := (temp_cl_dir / 'sort.xml')).touch()
    # The file is empty
    assert generator.generate_sort_xml(None)


def test_generate_sort_xml_none_file_exists_non_empty_sort_xml_returns_false(temp_cwd):
    temp_cl_dir = get_temp_changelist_dir_absolute_path(temp_cwd)
    (temp_sort_xml := (temp_cl_dir / 'sort.xml')).touch()
    temp_sort_xml.write_text('Hello Again, Reader!')
    # The file contains data
    assert generator.generate_sort_xml(None)


def test_generate_sort_xml_path_file_exists_non_empty_sort_xml_returns_false(temp_cwd):
    temp_cl_dir = get_temp_changelist_dir_absolute_path(temp_cwd)
    (temp_sort_xml := (temp_cl_dir / 'sort.xml')).touch()
    temp_sort_xml.write_text('Hello Again, Reader!')
    # The file contains data
    assert generator.generate_sort_xml(temp_sort_xml)


def test_generate_sort_xml_str_file_exists_non_empty_sort_xml_returns_false(temp_cwd):
    temp_cl_dir = get_temp_changelist_dir_absolute_path(temp_cwd)
    (temp_sort_xml := (temp_cl_dir / 'sort.xml')).touch()
    temp_sort_xml.write_text('Hello Again, Reader!')
    # The file contains data
    assert generator.generate_sort_xml(str(temp_sort_xml))