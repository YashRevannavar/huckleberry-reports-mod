from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

@dataclass
class Result(Generic[T]):
    """
    Standard Result object for error handling across services.
    :param success: Boolean representing if operation succeeded.
    :param data: The returned data if successful.
    :param error: The error string if failed.
    """
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
