import pytest

@pytest.mark.polarion(test_id="DEMO-391")
def test_if_true():
    assert 5 == 5


@pytest.mark.polarion(test_id="DEMO-392")
def test_if_false():
    assert 5 == 6


@pytest.mark.polarion(test_id="DEMO-393")
@pytest.mark.parametrize('value', [0, 10, 20, 25, 30])
def test_with_parametrize(value):
    assert True


@pytest.mark.polarion(test_id="DEMO-398")
@pytest.mark.parametrize('value', [0, 10, 20, 25, 30])
@pytest.mark.parametrize('value2', [0, 10, 20, 25, 30])
@pytest.mark.parametrize('value3', [0, 10, 20, 25, 30])
def test_with_parametrize(value, value2, value3):
    assert value < value2 or value == value3


# @pytest.mark.polarion(test_id="DEMO-654")
# def test_nonexistent():
#     '''Create to force pytest to fail when a test case
#      is not existent in Polarion'''
#     assert 5 == 6

@pytest.mark.skip
@pytest.mark.polarion(test_id="DEMO-394")
def test_if_broken_block():
    assert np.array([1,2,3,4,5])

@pytest.mark.skip
def test_tmp():
    from polarion.polarion import Polarion

    POLARION_HOST='http://desktop-ajbsmkv/polarion/'
    POLARION_USER='admin'
    POLARION_PASSWORD='admin'

    client = Polarion(polarion_url=POLARION_HOST,
                    user=POLARION_USER,
                    password=POLARION_PASSWORD)

    project = client.getProject('Demo2')

    test_case_id = "DEMO-391"
    test_case_item = project.getWorkitem(test_case_id)

    test_case_item.comments
