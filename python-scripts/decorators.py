import functools
import time
from typing import Final


WRAPER_TIME_MSG: Final = (
    "Elapsed time executing {function_name} function: {elapsed_time:0.4f} seconds"
)


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(
            WRAPER_TIME_MSG.format(
                function_name=func.__name__, elapsed_time=elapsed_time
            )
        )
        return value

    return wrapper_timer
