import pytest

@pytest.mark.polarion(test_id="TEST-391")
def test_if_true():
    assert 5 == 5
