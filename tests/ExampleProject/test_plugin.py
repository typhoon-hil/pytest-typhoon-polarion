import warnings
import pytest
from polarion import polarion
from polarion.record import Record
from src.exceptions import PolarionTestIDWarn

polarion_token = {
	"Tiarles_Polarion_Token": "eyJraWQiOiJiZmFiMGYyZS1jMGE4MDIxNy0zYzQ2NGZiNy00ZjRkNWEwOSIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJhZG1pbiIsImlkIjoiYmZhYzE5NDgtYzBhODAyMTctM2M0NjRmYjctOTkzMzY5M2YiLCJleHAiOjE2OTg4Nzk2MDAsImlhdCI6MTY5MTEzNzg3NH0.YN8i8YrMYcmRzla_7_92UJQ9hvOGJ9RiRgBlS5WEzigjoUgzqZswU-K2Y0R5vbEcLccDvsSHzzQQueHzNGq4zIOjzE9H74VMTFIBIPlm6oTSroILFBKFASlNdie27qnbMh4WmjFQCqiu2kHS5EgCbKqVUst8yxDMihJhfd7t92ZvcPp-YVxr0T8D7qgBqF77_9Mi20thlah3GN8YLA7UCQLFvI4JXn_hq2MCQABLUpl8CvMyATHp1AMjZOPMkDy70q9Nt_xBJZ2MoPGwiY5F4DKQ48f0PGs8ywIImRbDL1frGlphix8KFzEWnWJ0rGRulN_TL_bNYtJJquYWiE3tSw"
}


# pytest_to_polarion_test_cases = {
# 	'ExampleProject/test_plugin.py::test_sum': 'EP-392',
# 	'ExampleProject/test_plugin.py::test_square_root': 'EP-391',
# 	'aasnansnas': 'EP-300',
# }
#
# for key, item in pytest_to_polarion_test_cases.items():
# 	# print(item)
# 	print(key, item)
# 	try:
# 		test_case = run.getTestCase(item)
# 		if test_case is None:
# 			raise TypeError
# 		print("test_case.setResult(Record.ResultType.BLOCKED, 'Testing blocking')")
# 		# test_case.setResult(Record.ResultType.BLOCKED, 'Testing blocking')
# 	except TypeError as e:
# 		warnings.warn(f"Test ID {item} not founded in the selected Test Run Project!", PolarionTestIDWarn)
#
# print("Progressing ...")

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
