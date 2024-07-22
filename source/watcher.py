"""All functions and features for logging the app
"""
from loguru import logger

def log_decorator(**decorator_kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if hasattr(result, "headers"):  # returns True
                for key, value in decorator_kwargs.items():
                    print(key, value)
            else:
                print("kein header")
            print(result)
            return result
        return wrapper
    return decorator

# @log_decorator(info="Default Info", user="Default User")
# def my_func(value):
#     return value + 5

# Test the function
# print(my_func(10))  # This will print 15 and write 'Result: 15\ninfo: Default Info\nuser: Default User' to output.txt

def init_logging(log_level: str) -> None:
    """Initialization of logging to create log file and set level at beginning of the app.

    Args:
        log_level (str): Configured log level
    """
    logger.add("../files/henCommander.log", rotation="500 MB", level=log_level)
