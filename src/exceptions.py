
class PluginError(Exception):
    """Base exception class"""
    pass


class ConfigurationError(PluginError):
    """Errors in runtime configuration"""
    pass


class InvalidCredentialsError(Exception):
    """Errors in polarion credentials"""
    pass


class TestCaseTypeError(Exception):
    '''Error in Test Case result update 
    in case the Test Type is not configured as Automated'''
    pass

class TestCaseNotFoundError(Exception):
    '''Error in the validation of the test cases needed 
    for update on Polarion.'''
    pass
