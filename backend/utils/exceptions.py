class AppBaseError(Exception):
    """Base exception class for all application-specific errors."""
    pass


class PortalError(AppBaseError):
    """Raised when an error occurs during portal automation."""
    pass


class AuthenticationError(PortalError):
    """Raised when authentication with the portal fails."""
    pass


class DownloadError(PortalError):
    """Raised when downloading a report fails."""
    pass


class DataProcessingError(AppBaseError):
    """Raised when an error occurs during data processing."""
    pass


class ExcelValidationError(DataProcessingError):
    """Raised when an Excel file is missing required columns or has invalid data."""
    pass


class ChartGenerationError(AppBaseError):
    """Raised when an error occurs during chart generation."""
    pass


class PPTGenerationError(AppBaseError):
    """Raised when an error occurs during PPT generation."""
    pass


class CustomerNotFoundError(AppBaseError):
    """Raised when a requested customer is not found in the configuration or data."""
    pass


class ConfigurationError(AppBaseError):
    """Raised when there is an issue with the application configuration."""
    pass


class RetryExceededError(AppBaseError):
    """Raised when the maximum number of retries has been exceeded for an operation."""
    pass

class AutomationError(AppBaseError):
    """Raised when an error occurs during browser automation."""
    pass
