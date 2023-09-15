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
    assert value < 12 or value == 25


@pytest.mark.polarion(test_id="DEMO-666")
def test_nonexistent():
    assert 5 == 6
