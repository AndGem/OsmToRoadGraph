import time

from typing import Callable


def timer(function: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print("starting {}".format(function.__name__))

        result = function(*args, **kwargs)

        print(
            "finished {} in {}s".format(
                function.__name__, round(time.time() - start_time, 2)
            )
        )
        print("")

        return result

    return wrapper
