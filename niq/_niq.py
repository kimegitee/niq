import os
import sys
import json
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


def sort_file_names(src_dir):
    dst_dir = src_dir.strip('/') + '_sorted'
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    src_to_dst_dict = {}
    for src_path in glob(os.path.join(src_dir, '*')):
        if os.path.isfile(src_path):
            dst_path = os.path.basename(src_path)
            dst_path = ''.join(c for c in dst_path if c.isnumeric())
            if dst_path:
                src_to_dst_dict[src_path] = dst_path
    pad_length = max(len(path) for path in src_to_dst_dict.values())
    for src_path, dst_path in src_to_dst_dict.items():
        _, ext = os.path.splitext(src_path)
        dst_path = f'{int(dst_path):0{pad_length}d}{ext}'
        dst_path = os.path.join(dst_dir, dst_path)
        src_to_dst_dict[src_path] = dst_path
        shutil.copy(src_path, dst_path)
    src_to_dst_dict = {
        os.path.basename(k): os.path.basename(v) for k, v in src_to_dst_dict.items()
    }
    json_path = src_dir.strip('/') + '_map.json'
    json.dump(src_to_dst_dict, open(json_path, 'w'), indent=4, sort_keys=True)


def cache(func=None, cache_dir=Path.home() / '.niq'):
    '''Cache result of function call on disk
    Support multiple positional and keyword arguments'''
    if func is None:
        return partial(cache, cache_dir=cache_dir)

    def print_status(status, func, args, kwargs):
        logging.info(
            f'{status}\n'
            f'func   :: {func.__name__}\n'
            f'args   :: \n'
            f'{args}\n'
            f'kwargs :: \n'
            f'{kwargs}'
        )


    @wraps(func)
    def memoized_func(*args, **kwargs):
        if os.environ.get('NIQ_CACHE', '0') == '1':
            func_id = identify_func(func, args, kwargs)
            cache_path = os.path.join(cache_dir, func_id)
            if os.path.exists(cache_path) and not func.__name__ in os.environ:
                print_status('Using cached result', func, args, kwargs)
                return joblib.load(open(cache_path, 'rb'))
            else:
                print_status('Updating cache with fresh run', func, args, kwargs)
                result = func(*args, **kwargs)
                if not os.path.exists(cache_dir):
                    os.mkdir(cache_dir)
                joblib.dump(result, open(cache_path, 'wb'))
                return result
        else:
            print_status('Not using or updating cache ', func, args, kwargs)
            return func(*args, **kwargs)

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
        print(f'Calling {func.__name__} took {timed_func.last_run}')
        return result

    return timed_func

def identify(x):
    '''Return an hex digest of the input'''
    return xxhash.xxh64(pickle.dumps(x), seed=0).hexdigest()

def identify_func(func, args, kwargs):
    # Quick hack for unbound method case
    if args and (inspect.ismethod(func) or getattr(args[0], func.__name__, None)):
        args = args[1:]
    return identify((func.__name__, args, kwargs))
