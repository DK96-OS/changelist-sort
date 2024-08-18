""" Testing Workspace Tree.
"""
from xml.etree.ElementTree import fromstring
from changelist_sort.changelist_data import ChangelistData
from changelist_sort.workspace.workspace_tree import _convert_bool, _extract_change_data, _filter_project_dir, _find_changelist_manager, _write_list_element
from test.data_provider import get_multi_changelist_xml
from test.data_provider import get_no_changelist_xml, get_simple_changelist_xml


def test_find_changelist_manager_no_changelist_returns_none():
    xml_root = fromstring(get_no_changelist_xml())
    assert _find_changelist_manager(xml_root) is None


def test_find_changelist_manager_simple_changelist_returns_element():
    xml_root = fromstring(get_simple_changelist_xml())
    element = _find_changelist_manager(xml_root)
    cl_elements = list(element.iter())
    assert len(cl_elements) == 3
    assert cl_elements[0].attrib['name'] == 'ChangeListManager'
    assert cl_elements[1].tag == 'list'
    assert cl_elements[2].tag == 'change'


def test_find_changelist_manager_multi_changelist_returns_element():
    xml_root = fromstring(get_multi_changelist_xml())
    element = _find_changelist_manager(xml_root)
    cl_elements = list(element.iter())
    assert len(cl_elements) == 6
    cl_main = cl_elements[1]
    assert cl_main.tag == 'list'
    assert cl_elements[2].tag == 'change'
    assert cl_elements[3].tag == 'change'
    cl_test = cl_elements[4]
    assert cl_test.tag == 'list'
    assert cl_elements[5].tag == 'change'


def test_extract_change_data_simple_():
    xml_root = fromstring(get_simple_changelist_xml())
    element = _find_changelist_manager(xml_root)
    cl_elements = list(element.iter())
    # Extract Change Data is called on a List element
    c_data_list = _extract_change_data(cl_elements[1])
    assert len(c_data_list) == 1
    c_data0 = c_data_list[0]
    assert c_data0.before_path == '/main.py'
    assert c_data0.before_dir == False
    assert c_data0.after_path == '/main.py'
    assert c_data0.after_dir == False


def test_extract_change_data_empty_element_returns_empty_list():
    xml_root = fromstring(get_simple_changelist_xml())
    element = _find_changelist_manager(xml_root)
    cl_elements = list(element.findall('list'))
    assert len(cl_elements) == 1
    # Remove sub_element of the List element
    cl_elements[0].remove(cl_elements[0][0])
    assert len(cl_elements[0]) == 0
    assert len(_extract_change_data(cl_elements[0])) == 0


def test_write_list_element_simple_returns_element():
    cl_data = ChangelistData(
        id="9f60fda2-421e-4a4b-bd0f-4c8f83a47c88",
        name="Simple",
        changes=[],
        comment="Main Program Files",
        is_default=False,
    )
    cl_element = _write_list_element(cl_data)
    #
    assert len(cl_element.findall('change')) == 0
    assert cl_element.attrib['id'] == '9f60fda2-421e-4a4b-bd0f-4c8f83a47c88'
    assert cl_element.attrib['name'] == 'Simple'
    assert cl_element.attrib['comment'] == 'Main Program Files'
    # Default is not included when false
    assert 'default' not in cl_element.attrib


def test_filter_project_dir_none_returns_none():
    assert _filter_project_dir(None) is None


def test_filter_project_dir_normal_returns_shortened_path():
    normal_input = '$PROJECT_DIR$/main.py'
    assert _filter_project_dir(normal_input) == '/main.py'


def test_filter_project_dir_without_returns_same_path():
    test_input = '/main.py'
    assert _filter_project_dir(test_input) == '/main.py'


def test_convert_bool_none_returns_none():
    assert _convert_bool(None) is None


def test_convert_bool_false_returns_false():
    assert _convert_bool('false') == False


def test_convert_bool_true_returns_true():
    assert _convert_bool('true') == True
