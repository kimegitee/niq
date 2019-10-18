# niq

Available utilities:
- Cache function calls results on disk

## Installation
```bash
pip install 'niq@git+ssh://git@github.com/Cinnamon/niq.git@v1.0.0'
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
