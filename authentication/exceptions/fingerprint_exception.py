from user_platform.exceptions import BasePlatformException


class FingerprintException(BasePlatformException):
    def __init__(self, message, code="FINGERPRINT"):
        super().__init__(message, code)
