""" Testing Changelist Data Methods
"""
from changelist_sort.changelist_data import ChangelistData


def test_get_simple_name_empty_returns_empty():
    instance = ChangelistData(
        id='1234',
        name='',
        changes=[],
    )
    assert '' == instance.get_simple_name()


def test_get_simple_name_space_returns_empty():
    instance = ChangelistData(
        id='1234',
        name=' ',
        changes=[],
    )
    assert '' == instance.get_simple_name()


def test_get_simple_name_allcaps_returns_lower():
    instance = ChangelistData(
        id='1234',
        name='ALLCAPS',
        changes=[],
    )
    assert 'allcaps' == instance.get_simple_name()


def test_get_simple_name_trailspace_returns_word():
    instance = ChangelistData(
        id='1234',
        name='Trailspace ',
        changes=[],
    )
    assert 'trailspace' == instance.get_simple_name()
