import os
import sys
import json
import shutil
import pickle
import xxhash
from glob import glob
from time import time
from functools import wraps

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
    src_to_dst_dict = {os.path.basename(k):os.path.basename(v) for k, v in src_to_dst_dict.items()}
    json_path = src_dir.strip('/') + '_map.json'
    json.dump(src_to_dst_dict, open(json_path, 'w'), indent=4, sort_keys=True)


def memoize(func):
    '''Cache result of function call on disk
    Support multiple positional and keyword arguments'''

    def print_status(status, func, args, kwargs):
        print(f'{status}\n'
              f'func   :: {func.__name__}\n'
              f'args   :: \n'
              f'{args}\n'
              f'kwargs :: \n'
              f'{kwargs}')

    def identify(x):
        '''Return an hex digest of the input'''
        return xxhash.xxh64(pickle.dumps(x), seed=0).hexdigest()

    @wraps(func)
    def memoized_func(*args, **kwargs):
        cache_dir = 'cache'
        try:
            os.environ['DEBUG']
            print('Environment variable DEBUG is set, will use cache when possible\n'
                  'To invalidate cache, add the function name as an environment variable')
            func_id = identify((func.__name__, args, kwargs))
            cache_path = os.path.join(cache_dir, func_id)
            if (os.path.exists(cache_path) 
                    and not func.__name__ in os.environ
                    and not 'BUST_CACHE' in os.environ):
                print_status('Using cached result', func, args, kwargs)
                return pickle.load(open(cache_path, 'rb'))
            else:
                print_status('Updating cache with fresh run', func, args, kwargs)
                result = func(*args, **kwargs)
                if not os.path.exists(cache_dir):
                    os.mkdir(cache_dir)
                pickle.dump(result, open(cache_path, 'wb'))
                return result
        except (KeyError, AttributeError, TypeError):
            print_status('Not using or updating cache ', func, args, kwargs)
            return func(*args, **kwargs)

    return memoized_func

def howlong(func):
    '''Decorator to print a function's execution time'''

    @wraps(func)
    def timed_func(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        stop_time = time()
        print(f'Calling {func.__name__} took {stop_time - start_time}')
        return result

    return timed_func
