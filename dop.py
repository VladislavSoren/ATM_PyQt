import time
from functools import wraps


def log_time(logger, description=''):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            logger.info(f'Start parsing {description} ({func.__name__})')
            result = func(*args, **kwargs)
            end = time.time()
            exec_time = round(end - start, 2)
            logger.info(f'Parsing time {description} ({func.__name__}): {exec_time}s')
            return result
        return wrapper
    return inner