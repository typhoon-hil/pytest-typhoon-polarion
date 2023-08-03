
class PluginWarning(Warning):
    """Base exception class"""
    pass


class PolarionTestIDWarn(PluginWarning):
    """Throw when test_id used is not found in the test run"""
    pass
