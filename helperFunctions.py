import time
from functools import wraps

def log_stats(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        print(f"Called function: {func.__name__}")
        print(f"Arguments: {args}, {kwargs}")
        print(f"Return value: {result}")
        print(f"Execution time: {end_time - start_time:.2f} seconds")

        return result

    return wrapper
