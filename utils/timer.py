import time


def timer(active):
    def timer_decorator(function):
        def wrapper(*args, **kwargs):
            if active:
                start_time = time.time()
                print("")
                print("starting {}".format(function.__name__))

            result = function(*args, **kwargs)

            if active:
                print("finished {} in {}s".format(function.__name__, round(time.time() - start_time, 2)))
                print("")

            return result
        return wrapper
    return timer_decorator
