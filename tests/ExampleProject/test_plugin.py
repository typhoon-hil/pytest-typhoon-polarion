import pytest




# run.records[0].setResult(Record.ResultType.PASSED, 'Pass expected')
# run.records[1].setResult(Record.ResultType.PASSED, 'Pass expected')
#
#
# run = project.getTestRun('SWQ-0001')
#
# plan = project.getPlan('00002')

# Settings.POLARION_HOST = ''
# Settings.POLARION_USER = ''
# Settings.POLARION_PASSWORD = ''
#     # POLARION_TOKEN = ''
#     POLARION_PROJECT_ID = ''
#     POLARION_TEST_RUN = ''



def soma_fnc(param1, param2):
	return param1 + param2


# @pytest.mark.parametrize("param1", [1, 2])
# @pytest.mark.parametrize("param2", [3, 4])
@pytest.mark.polarion(test_id='EP-392')
@pytest.mark.sum_fnc
def test_sum():
	param1 = 2
	param2 = 9

	assertion = soma_fnc(param1, param2) == (param1 + param2)

	# client = polarion.Polarion('http://localhost:80/polarion', 'admin', 'admin')
	# project = client.getProject("BasicProject")
	# workitem1 = project.getWorkitem("BP-12")

	assert assertion


@pytest.mark.polarion(test_id='EP-391')  #
def test_square_root():
	amp = 1
	freq = 60

	from typhoon.test.signals import pandas_sine
	import typhoon.test.harmonic as harmonic
	signal = pandas_sine(amplitude=amp, frequency=50)

	content = harmonic.frequency_content(signal, 240)

	# client = polarion.Polarion('http://localhost:80/polarion', 'admin', 'admin')
	# project = client.getProject("BasicProject")
	# workitem1 = project.getWorkitem("BP-12")

	assert pytest.approx(0, rel=1e-6) == content(0) and pytest.approx(0, rel=1e-6) == content(120) and pytest.approx(0, rel=1e-6) == content(240), "Harmonics detected"
	assert abs(content(60)) == amp, "60 Hz amplitude not correct"

	# assert assertion
