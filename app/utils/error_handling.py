# utils/error_handling.py
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from functools import wraps

logger = logging.getLogger(__name__)

def handle_api_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"API error in {func.__name__}: {str(e)}")
            raise
    return wrapper

class ErrorHandler:
    @retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=4, max=10))
    def api_call_with_retry(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"API call failed: {str(e)}")
            raise