from cProfile import Profile
from io import StringIO
from pstats import Stats
from time import perf_counter
from functools import wraps

def profile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        s = StringIO()
        ps = Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        print(s.getvalue())
        return result
    return wrapper


def showArgs(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f'Argument(s) of function "{func.__name__}: {args, kwargs}"')
        return result
    return wrapper


def secTimer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _start = perf_counter()
        result = func(*args, **kwargs)
        _end = perf_counter()
        print(f'Runtime of function "{func.__name__}" (secounds): {_end-_start}.')
        return result
    return wrapper
