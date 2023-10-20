
class PluginError(Exception):
    """Base exception class"""
    pass


class ConfigurationError(PluginError):
    """Errors in runtime configuration"""
    pass


class InvalidCredentialsError(PluginError):
    """Errors in polarion credentials"""
    pass


class TestCaseTypeError(PluginError):
    '''Error in Test Case result update 
    in case the Test Type is not configured as Automated'''
    pass

class TestCaseNotFoundError(PluginError):
    '''Error in the validation of the test cases needed 
    for update on Polarion.'''
    pass
