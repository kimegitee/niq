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

def test_bound_method_cache_should_hit(d):
    class C:
        def f(_):
            return now()
    c = C()
    c.f = cache(cache_dir=d)(c.f)
    assert c.f() == c.f()

def test_bound_method_cache_should_miss(d):
    class C:
        def f(_, x):
            return x
    c = C()
    c.f = cache(cache_dir=d)(c.f)
    assert c.f(1) != c.f(2)

def test_unbound_method_cache_should_hit(d):
    class C:
        @cache(cache_dir=d)
        def f(_):
            return now()
    c = C()
    assert c.f() == c.f()

def test_unbound_method_cache_should_miss(d):
    class C:
        @cache(cache_dir=d)
        def f(_, x):
            return x
    c = C()
    assert c.f(1) != c.f(2)

def test_ignored_function_should_miss(d):
    f = cache(cache_dir=d)(now)
    os.environ['NIQ_REFRESH'] = 'now'
    assert f() != f()

@pytest.mark.xfail
def test_different_instance(d):
    class C:
        @cache(cache_dir=d)
        def f(_, x):
            return x + now()
    c1 = C()
    c2 = C()
    assert c1.f(1) != c2.f(1)

def test_same_method_different_class(d):
    class A:
        @cache(cache_dir=d)
        def f(_):
            return 'A'
    class B:
        @cache(cache_dir=d)
        def f(_):
            return 'B'
    assert A().f() != B().f()

def test_different_function_same_arg(d):
    @cache
    def f(x):
        return x
    @cache
    def g(x):
        return x + 1
    assert f(1) != g(1)
