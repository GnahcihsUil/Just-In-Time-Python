from Interval import Interval
from numba import types
from numba.extending import typeof_impl, as_numba_type
from numba.extending import type_callable


class IntervalType(types.Type):
    def __init__(self):
        super(IntervalType, self).__init__(name='Interval')


interval_type = IntervalType()


# This is the function that Numba will call to get the type of an Interval
# infer numba type of python object
# runtime
@typeof_impl.register(Interval)
def typeof_index(val, c):
    return interval_type


# infer the Numba type of Python types
# compile time
as_numba_type.register(Interval, interval_type)


@type_callable(Interval)
def type_interval(context):
    def typer(lo, hi):
        if isinstance(lo, types.Float) and isinstance(hi, types.Float):
            return interval_type
    return typer
