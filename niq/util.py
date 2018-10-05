import os
import sys
import json
import shutil
import pickle
import xxhash
from glob import glob
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
    Supports single argument function only'''

    def identify(x):
        '''Return an hex digest of the input'''
        x = x if isinstance(x, str) else x.tostring() # Hashing numpy array
        return xxhash.xxh64(x, seed=0).hexdigest()

    @wraps(func)
    def memoized_func(arg):
        cache_dir = 'cache'
        try:
            os.environ['DEBUG']
            func_id = identify(func.__name__)
            arg_id = identify(arg)
            cache_path = os.path.join(cache_dir, func_id + arg_id + '.pkl')
            if os.path.exists(cache_path):
                print('DEBUG ENV is set, using cache\n'
                     f'function :: {func.__name__}\n'
                     f'argument :: {arg}\n'
                     f'type     :: {type(arg)}')
                return pickle.load(open(cache_path, 'rb'))
            else:
                print('Not using cache')
                result = func(arg)
                if not os.path.exists(cache_dir):
                    os.mkdir(cache_dir)
                pickle.dump(result, open(cache_path, 'wb'))
                return result
        except (KeyError, AttributeError, TypeError):
            print('Not using cache')
            return func(arg)

    return memoized_func
