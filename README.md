[![kimegitee](https://circleci.com/gh/kimegitee/niq.svg?style=shield)](https://circleci.com/gh/kimegitee/niq)

# niq

Available utilities:
- Cache function calls results on disk

## Installation
```bash
pip install niq
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
