import logging
import time
from functools import wraps
from typing import Callable

logger = logging.getLogger(__name__)


def retriable(retries: int, rest_between: int, fail_on_error: bool = True) -> Callable:
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs) -> Callable:
            attempt = retries
            reason = None
            while attempt:
                try:
                    return func(*args, **kwargs)
                except Exception as ex:
                    reason = str(ex)
                    attempt -= 1
                    time.sleep(rest_between)
            if fail_on_error:
                raise Exception(f'Failed after {retries} retries. {reason}')
            else:
                logger.warning(f'Failed after {retries} retries. {reason}')

        return wrapped

    return wrapper
