from numba import jit
from Interval import Interval
import time

@jit(nopython=True)
def inside_interval(interval, x):
    return interval.start <= x < interval.end


def inside_interval_py(interval, x):
    return interval.start <= x < interval.end


@jit(nopython=True)
def interval_width(interval):
    return interval.length


@jit(nopython=True)
def sum_intervals(i, j):
    return Interval(i.start + j.start, i.end + j.end)


def sum_intervals_py(i, j):
    return Interval(i.start + j.start, i.end + j.end)

@jit(nopython=True)
def pythagorean_triples_in_interval(i):
    triples = []
    for a in range(int(i.start), int(i.end)):
        for b in range(a, int(i.end)):
            c = (a ** 2 + b ** 2) ** 0.5
            if inside_interval(i, c):
                triples.append((a, b, c))
    return triples


def pythagorean_triples_in_interval_py(i):
    triples = []
    for a in range(int(i.start), int(i.end)):
        for b in range(a, int(i.end)):
            c = (a ** 2 + b ** 2) ** 0.5
            if inside_interval_py(i, c):
                triples.append((a, b, c))
    return triples


if __name__ == '__main__':
    i = Interval(10, 10000)
    st = time.time()
    for _ in range(10):
        pythagorean_triples_in_interval(i)
    print(time.time() - st)

    st = time.time()
    for _ in range(10):
        pythagorean_triples_in_interval_py(i)
    print(time.time() - st)
