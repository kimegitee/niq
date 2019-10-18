# niq

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
The memoize decorator saves the function result in ~/.niq and loads it if environment variable NIQ_CACHE is set to 1.

Supports multi-arity functions.
