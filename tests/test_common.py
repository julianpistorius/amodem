from amodem import common
import numpy as np


def iterlist(x, *args, **kwargs):
    x = np.array(x)
    return list((i, list(x)) for i, x in common.iterate(x, *args, **kwargs))


def test_iterate():
    N = 10
    assert iterlist(range(N), 1) == [
        (i, [i]) for i in range(N)]

    assert iterlist(range(N), 2) == [
        (i, [i, i+1]) for i in range(0, N-1, 2)]

    assert iterlist(range(N), 3) == [
        (i, [i, i+1, i+2]) for i in range(0, N-2, 3)]

    assert iterlist(range(N), 1, func=lambda b: -np.array(b)) == [
        (i, [-i]) for i in range(N)]


def test_split():
    L = [(i*2, i*2+1) for i in range(10)]
    iters = common.split(L, n=2)
    assert list(zip(*iters)) == L

    for i in [0, 1]:
        iters = common.split(L, n=2)
        next(iters[i])
        try:
            next(iters[i])
            assert False
        except IndexError as e:
            assert e.args == (i,)


def test_icapture():
    x = range(100)
    y = []
    z = []
    for i in common.icapture(x, result=y):
        z.append(i)
    assert list(x) == y
    assert list(x) == z


def test_dumps_loads():
    x = np.array([.1, .4, .2, .6, .3, .5])
    y = common.loads(common.dumps(x))
    assert all(x == y)


def test_saturation():
    x = np.array([1, -1, 1, -1]) * 1e10
    try:
        common.check_saturation(x)
        assert False
    except common.SaturationError as e:
        assert e.args == (max(x),)

def test_izip():
    x = range(10)
    y = range(-10, 0)
    assert list(common.izip([x, y])) == list(zip(x, y))
