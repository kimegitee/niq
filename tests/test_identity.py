import os
import time
import pytest
from niq import cache
from niq import identify_func
from tempfile import TemporaryDirectory


os.environ['NIQ_CACHE'] = '1'


@pytest.fixture
def d():
    with TemporaryDirectory() as d:
        yield d

def now():
    return time.time()

def test_custom_cache_dir(d):
    f = cache(cache_dir=d)(now)
    assert f() == f()

def test_caching_bound_method(d):
    class C:
        def f(_):
            return now()
    f = cache(cache_dir=d)(C().f)
    assert f() == f()

def test_caching_unbound_method(d):
    class C:
        @cache(cache_dir=d)
        def f(_):
            return now()
    assert C().f() == C().f()
