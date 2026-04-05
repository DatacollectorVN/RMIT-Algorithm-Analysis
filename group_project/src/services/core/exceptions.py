"""Domain-specific exceptions for the similarity search services."""


class LookalikeSearchError(Exception):
    """Base class for all recoverable errors in this package."""

    pass


class ValidationError(LookalikeSearchError):
    """Raised when inputs, corpus records, or query payloads are invalid."""

    pass
