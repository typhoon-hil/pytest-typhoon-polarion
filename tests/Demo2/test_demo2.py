import pytest


@pytest.mark.polarion(test_id="DEMO-391")
def test_if_true():
    assert 5 == 5


@pytest.mark.polarion(test_id="DEMO-393")
def test_if_false():
    assert 5 == 6


@pytest.mark.polarion(test_id="DEMO-394")
@pytest.mark.parametrize('value', [0, 10, 20, 25, 30])
def test_with_parametrize(value):
    '''This test case is under development. Only the first test 
    (`value = 0` will be considered) when upload on Polarion.'''
    assert value < 12 or value == 25
