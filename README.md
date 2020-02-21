[![Cinnamon](https://circleci.com/gh/Cinnamon/niq.svg?style=shield&circle-token=a45c432116f07b0dba9165f22f1707a288c4618a)](https://circleci.com/gh/Cinnamon/niq)

# niq

Available utilities:
- Cache function calls results on disk

## Installation
```bash
pip install 'niq@git+ssh://git@github.com/Cinnamon/niq.git@master'
```
## Usage

```python
from niq import cache

@cache
def f():
    pass
```

By default the cache decorator saves the function result in `~/.niq` and loads it if environment variable `NIQ_CACHE` is set to 1.

You can customize cache location with the `cache_dir` parameter

```python
@cache(cache_dir='/path/to/custom/cache_dir')
def f():
    pass
```

## Tests

Tests are available under `tests/`, use `pytest` to run them
