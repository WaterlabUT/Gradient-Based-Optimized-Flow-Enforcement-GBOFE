"""
Custom exceptions for DEM processing.
"""

class DEMProcessingError(Exception):
    """Base exception for DEM processing errors."""
    pass

class InvalidFileFormatError(DEMProcessingError):
    """Raised when the file format is not compatible."""
    pass

class IncompatibleCRSError(DEMProcessingError):
    """Raised when coordinate systems are not compatible."""
    pass

class InvalidParameterError(DEMProcessingError):
    """Raised when provided parameters are not valid."""
    pass

class FileNoFoundError(DEMProcessingError):
    """Raised when a required file does not exist."""
    pass
