import cProfile
from io import StringIO
from pstats import Stats
from time import perf_counter

def profile(func, sortby: str='cumulative'):

    """A decorator that uses cProfile to profile a function"""
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = func(*args, **kwargs)
        s = StringIO()
        ps = Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return wrapper


def profileSec(func):

    """A decorator that measures the time it takes to run a function"""
    def wrapper(*args, **kwargs):
        _start = perf_counter()
        retval = func(*args, **kwargs)
        _end = perf_counter()
        print(f'Time passed (secounds): {_end-_start}')
        return retval

    return wrapper
