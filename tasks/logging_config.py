import logging
from functools import wraps
from typing import Any, Callable, ParamSpec, TypeVar

from django.http import HttpRequest, HttpResponse

# Set up logger
logger = logging.getLogger('tasks')


# Type variables for the decorator
P = ParamSpec('P')
R = TypeVar('R', bound=HttpResponse)

def log_view_action(action_name: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Log view actions with consistent formatting.

    Args:
        action_name: Description of the view action being performed.

    Returns:
        A decorator function that wraps view functions and adds logging.

    """
    def decorator(view_func: Callable[P, R]) -> Callable[P, R]:
        @wraps(view_func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Extract request from args (first argument should be request)
            request = args[0] if args else kwargs.get('request')
            if not isinstance(request, HttpRequest):
                raise TypeError("First argument must be an HttpRequest")

            user_id = request.user.id if request.user.is_authenticated else 'anonymous'

            # Log the start of the action
            logger.info(
                f"View Action: {action_name} | "  # noqa: G004
                f"User: {user_id} | "
                f"Method: {request.method} | "
                f"Path: {request.path} | "
                f"Args: {args[1:]} | "  # Skip request arg
                f"Kwargs: {kwargs}",
            )

            try:
                response = view_func(*args, **kwargs)
                # Log successful completion
                logger.info(
                    f"Success: {action_name} | "  # noqa: G004
                    f"User: {user_id} | "
                    f"Status: {response.status_code}",
                )
                return response
            except Exception as e:
                # Log any errors that occur
                logger.exception(
                    f"Error in {action_name} | "  # noqa: G004
                    f"User: {user_id} | "
                    f"Error: {str(e)}",
                )
                raise

        return wrapper
    return decorator
