import os
import sys
import json
import types
import shutil
import pickle
import joblib
import xxhash
import inspect
import logging
from glob import glob
from time import time
from pathlib import Path
from functools import partial, wraps

CACHE_DIR = Path.home()/'.niq'

def load_cache(cache_path):
    try:
        return joblib.load(open(cache_path, 'rb'))
    except:
        return None

def save_cache(cache_path, result):
    cache_dir = os.path.dirname(cache_path)
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    joblib.dump(result, open(cache_path, 'wb'))

def cache(func=None, cache_dir=CACHE_DIR):
    '''Cache result of function call on disk
    Support multiple positional and keyword arguments'''
    if func is None:
        return partial(cache, cache_dir=cache_dir)


    @wraps(func)
    def memoized_func(*args, **kwargs):
        func_id = identify_func(func, args, kwargs)
        use_cache = os.environ.get('NIQ_CACHE', '0') == '1'
        refresh_list = os.environ.get('NIQ_REFRESH', '').split(',')
        cache_path = os.path.join(cache_dir, func_id)
        if use_cache:
            if func.__qualname__ in refresh_list:
                result = None
            else:
                result = load_cache(cache_path)
            if result is None:
                result = func(*args, **kwargs)
                save_cache(cache_path, result)
        else:
            result = func(*args, **kwargs)
        return result

    return memoized_func


def howlong(func):
    '''Decorator to print a function's execution time

    Time taken for the most recent call to the decorated function can be accessed via the `last_run` attribute'''

    @wraps(func)
    def timed_func(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        stop_time = time()
        timed_func.last_run = stop_time - start_time
        print(f'Calling {func.__qualname__} took {timed_func.last_run}')
        return result

    return timed_func

def identify(x):
    '''Return an hex digest of the input'''
    return xxhash.xxh64(pickle.dumps(x), seed=0).hexdigest()

def identify_func(func, args, kwargs):
    if '.' in func.__qualname__ and not inspect.ismethod(func):
       args = args[1:]
    return identify((func.__qualname__, args, kwargs))
