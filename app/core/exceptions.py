from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class CloudCompanionException(Exception):
    """Base exception for Cloud Companion"""

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(CloudCompanionException):
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict] = None):
        super().__init__(
            message=message,
            error_code="AUTH_ERROR",
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details,
        )


class AuthorizationError(CloudCompanionException):
    def __init__(self, message: str = "Insufficient permissions", details: Optional[Dict] = None):
        super().__init__(
            message=message,
            error_code="AUTHZ_ERROR",
            status_code=status.HTTP_403_FORBIDDEN,
            details=details,
        )


class ResourceNotFoundError(CloudCompanionException):
    def __init__(self, resource: str = "Resource", details: Optional[Dict] = None):
        super().__init__(
            message=f"{resource} not found",
            error_code="NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            details=details,
        )


class ValidationError(CloudCompanionException):
    def __init__(self, message: str = "Validation failed", details: Optional[Dict] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details,
        )


class DatabaseError(CloudCompanionException):
    def __init__(self, message: str = "Database operation failed", details: Optional[Dict] = None):
        super().__init__(
            message=message,
            error_code="DB_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details,
        )


class CloudAPIError(CloudCompanionException):
    def __init__(self, provider: str, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=f"{provider} API error: {message}",
            error_code="CLOUD_API_ERROR",
            status_code=status.HTTP_502_BAD_GATEWAY,
            details=details,
        )


class LLMError(CloudCompanionException):
    def __init__(self, message: str = "LLM operation failed", details: Optional[Dict] = None):
        super().__init__(
            message=message,
            error_code="LLM_ERROR",
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details,
        )


def create_error_response(exc: CloudCompanionException) -> Dict[str, Any]:
    return {
        "error": {
            "code": exc.error_code,
            "message": exc.message,
            "details": exc.details,
        }
    }
