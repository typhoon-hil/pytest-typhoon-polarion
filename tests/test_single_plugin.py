import pytest

@pytest.mark.polarion(test_id="TD-391")
def test_if_true():
    assert 5 == 5
