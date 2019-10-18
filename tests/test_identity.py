from niq import cache
from tempfile import TemporaryDirectory


def identity(x):
    return x


def test_decorating_with_custom_cache_dir():
    f = identity
    x = 1
    with TemporaryDirectory() as d:
        assert cache(cache_dir=d)(f)(x) == f(x)


def test_decorating_without_custom_cache_dir():
    f = identity
    x = 1
    assert cache(f)(x) == f(x)
