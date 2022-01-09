import time

from typing import Callable


def timer(function: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print(f"starting {function.__name__}")

        result = function(*args, **kwargs)

        print(f"finished {function.__name__} in {round(time.time() - start_time, 2)}s")
        print("")

        return result

    return wrapper
