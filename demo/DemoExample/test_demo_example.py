import pytest
from typhoon.test.signals import pandas_sine
import typhoon.test.harmonic as harmonic


@pytest.mark.polarion(test_id="DE-391")  # ID from the Polarion Test Case
def test_check_vab_freq():
    amp = 1
    freq = 60

    # Signal is an API generated signal, can also be capture from HIL Simulation
    signal = pandas_sine(amplitude=amp, frequency=freq, Ts=1e-3)

    # Frequency Analysis
    content = harmonic.frequency_content(signal, 240)

    assert abs(content(60)) == amp, "60 Hz amplitude not correct"
