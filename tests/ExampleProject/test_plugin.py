import pytest
# from polarion import polarion
# from polarion.record import Record

# client = polarion.Polarion('http://localhost:80/polarion', 'admin', 'admin')
#
# project = client.getProject("ExampleProject")
#
# # workitem1 = project.getWorkitem("EP-392")
# # workitem2 = project.getWorkitem("EP-391")
#
# run = project.getTestRun('REL')
#
# run.records[0].setResult(Record.ResultType.PASSED, 'Pass expected')
# run.records[1].setResult(Record.ResultType.PASSED, 'Pass expected')
#
#
# run = project.getTestRun('SWQ-0001')
#
# plan = project.getPlan('00002')


def soma_fnc(param1, param2):
	return param1 + param2


@pytest.mark.parametrize("param1", [1, 2])
@pytest.mark.parametrize("param2", [3, 4])
@pytest.mark.polarion('BP-12')
def test_quare_root(param1, param2):
	assertion = soma_fnc(param1, param2) == (param1 + param2)

	# client = polarion.Polarion('http://localhost:80/polarion', 'admin', 'admin')
	# project = client.getProject("BasicProject")
	# workitem1 = project.getWorkitem("BP-12")

	assert assertion
