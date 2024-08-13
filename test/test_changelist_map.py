""" Testing Changelist Map
"""
from changelist_sort.changelist_data import ChangelistData
from changelist_sort.changelist_map import ChangelistMap


def test_insert_simple_returns_true():
    instance = ChangelistMap()
    assert instance.insert(ChangelistData(
        id='1234',
        name='Build Updates',
        changes=[],
    ))


def test_insert_twice_returns_false():
    instance = ChangelistMap()
    assert instance.insert(ChangelistData(
        id='1234',
        name='Build Updates',
        changes=[],
    ))
    assert not instance.insert(ChangelistData(
        id='1234',
        name='Build Updates',
        changes=[],
    ))


def test_search_empty_returns_none():
    instance = ChangelistMap()
    assert instance.search(' ') is None
    assert instance.search('') is None
    assert instance.search('a') is None
    assert instance.search('root') is None
    assert instance.search('project root') is None
    assert instance.search('gradle') is None


def test_search_simple_returns_changelist():
    instance = ChangelistMap()
    assert instance.insert(ChangelistData(
        id='1234',
        name='Build Updates',
        changes=[],
    ))
    assert instance.search('buildupdates') is not None


def test_contains_id_empty_returns_false():
    instance = ChangelistMap()
    assert not instance.contains_id('1234')


def test_contains_id_simple_returns_true():
    instance = ChangelistMap()
    assert instance.insert(ChangelistData(
        id='1234',
        name='Build Updates',
        changes=[],
    ))
    assert instance.contains_id('1234')


def test_get_lists_empty_returns_empty():
    instance = ChangelistMap()
    assert 0 == len(instance.get_lists())


def test_get_lists_simple_returns_list():
    instance = ChangelistMap()
    assert instance.insert(ChangelistData(
        id='1234',
        name='Build Updates',
        changes=[],
    ))
    assert 1 == len(instance.get_lists())


def test_generate_new_id_then_insert_times_n():
    instance = ChangelistMap()
    for i in range(100):
        result = instance._generate_new_id()
        assert 36 == len(result)
        assert not instance.contains_id(result)
        instance.insert(
            ChangelistData(
                id=result,
                name='',
                changes=[]
            )
        )
        assert instance.contains_id(result)
