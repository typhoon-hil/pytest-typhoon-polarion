
class PluginError(Exception):
    """Base exception class"""
    pass


class ConfigurationError(PluginError):
    """Errors in runtime configuration"""
    pass


class InvalidCredentialsError(Exception):
    """Errors in polarion credentials"""
    pass
