class ATSServiceError(Exception):
    pass

class AuthenticationError(ATSServiceError):
    pass

class ATSAPIError(ATSServiceError):
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code

class ValidationError(ATSServiceError):
    pass

class ConfigurationError(ATSServiceError):
    pass
