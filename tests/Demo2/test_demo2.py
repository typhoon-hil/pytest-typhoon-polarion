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


@pytest.mark.polarion(test_id="DEMO-394")
@pytest.mark.parametrize('value', [0, 10, 20, 25, 30])
def test_with_parametrize(value):
    assert value < 12 or value == 25


# @pytest.mark.polarion(test_id="DEMO-654")
# def test_nonexistent():
#     '''Create to force pytest to fail when a test case
#      is not existent in Polarion'''
#     assert 5 == 6


@pytest.mark.polarion(test_id="DEMO-400")
def test_if_broken_block():
    assert np.array([1,2,3,4,5])
