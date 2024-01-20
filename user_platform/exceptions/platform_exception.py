class BasePlatformException(Exception):
    """Base exception class for the project."""

    def __init__(self, message, code="UNKNOWN"):
        super().__init__(message)
        self.code = code
