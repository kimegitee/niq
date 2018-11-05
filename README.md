# niq

## Installation
```bash
pip install https://github.com/kimegitee/niq/archive/master.zip
```
## Usage

```python
from niq.util import memoize

@memoize
def some_func():
    pass
```
The memoize decorator saves the function result in ~/project_root/cache and loads it if environment varible DEBUG is set to any value.

Supports multi-arity functions.
