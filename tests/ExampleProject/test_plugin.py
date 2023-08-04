import pytest


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

	assert assertion


@pytest.mark.polarion(test_id='EP-391')  #
def test_square_root():
	amp = 1
	freq = 60

	from typhoon.test.signals import pandas_sine
	import typhoon.test.harmonic as harmonic
	signal = pandas_sine(amplitude=amp, frequency=55, Ts=1e-3)

	content = harmonic.frequency_content(signal, 240)

	assert pytest.approx(0, rel=1e-6) == content(0) and pytest.approx(0, rel=1e-6) == content(120) and pytest.approx(0, rel=1e-6) == content(240), "Harmonics detected"
	assert abs(content(60)) == amp, "60 Hz amplitude not correct"


@pytest.mark.polarion(test_id="EP-393")
def test_pass():
	assert True


@pytest.mark.polarion(test_id="EP-394")
def test_fail():
	assert False


@pytest.mark.polarion(test_id="EP-395")
def test_blocked():
	np.array([1,2,3,4])
