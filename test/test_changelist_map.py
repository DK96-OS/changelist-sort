""" Testing Changelist Map
"""
from changelist_sort.changelist_data import ChangelistData
from changelist_sort.changelist_map import ChangelistMap
from test import data_provider


def test_insert_simple_returns_true():
    instance = ChangelistMap()
    assert instance.insert(ChangelistData(
        id='1234',
        name='Build Updates',
    ))


def test_insert_twice_same_id_returns_false():
    instance = ChangelistMap()
    same_id = instance._generate_new_id()
    assert instance.insert(ChangelistData(
        id=same_id,
        name='Module',
    ))
    assert not instance.insert(ChangelistData(
        id=same_id,
        name='App',
    ))


def test_insert_twice_different_id_same_name_returns_false():
    instance = ChangelistMap()
    init_cl = data_provider.get_module_changelist()
    assert instance.insert(init_cl)
    # Insert New CL with different id, same name
    new_cl = ChangelistData(
        id=instance._generate_new_id(),
        name=init_cl.name,
    )
    assert not instance.insert(new_cl)


def test_insert_gradle_changelists_returns():
    instance = ChangelistMap()
    gradle_cl = data_provider.get_multiple_gradle_changelists()
    assert len(gradle_cl) == 2
    assert instance.insert(gradle_cl[0])
    assert not instance.insert(gradle_cl[1])    # Has the Same Changelist Name
    #
    result = instance.search(gradle_cl[0].list_key.key)
    assert result.name == gradle_cl[0].name # The first in the list is returned


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
    ))
    assert 1 == len(instance.get_lists())


def test_generate_new_id_then_insert_times_n():
    instance = ChangelistMap()
    for i in range(100):
        result = instance._generate_new_id()
        assert 36 == len(result)
        assert not instance.contains_id(result)
        assert instance.insert(
            ChangelistData(
                id=result,
                name=f'{i}',    # A new name is required each time too
            )
        )
        assert instance.contains_id(result)
