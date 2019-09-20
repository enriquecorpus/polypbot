import functools
import datetime


def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('LOG [{date_time}]: Running job {f}'.format(f=func.__name__, date_time=datetime.datetime.now()))
        result = func(*args, **kwargs)
        print('LOG [{date_time}]: Job completed {f}'.format(f=func.__name__, date_time=datetime.datetime.now()))
        return result

    return wrapper
