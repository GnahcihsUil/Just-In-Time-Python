import time
from numba.extending import box
from numba.extending import unbox, NativeValue
from numba.core import cgutils
from numba.extending import lower_builtin
from Interval import Interval
from numba import types
from numba.extending import typeof_impl, as_numba_type, type_callable, models, register_model, make_attribute_wrapper
from numba import jit


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
    def typer(start, end):
        if isinstance(start, types.Float) and isinstance(end, types.Float):
            return interval_type
    return typer


@register_model(IntervalType)
class IntervalModel(models.StructModel):
    def __init__(self, dmm, fe_type):
        members = [
            ('start', types.float64),
            ('end', types.float64),
        ]
        models.StructModel.__init__(self, dmm, fe_type, members)


make_attribute_wrapper(IntervalType, 'start', 'start')
make_attribute_wrapper(IntervalType, 'end', 'end')


@lower_builtin(Interval, types.Float, types.Float)
def impl_interval(context, builder, sig, args):
    typ = sig.return_type
    start, end = args
    interval = cgutils.create_struct_proxy(typ)(context, builder)
    interval.start = start
    interval.end = end
    return interval._getvalue()


@unbox(IntervalType)
def unbox_interval(typ, obj, c):
    """
    Convert a Interval object to a native interval structure.
    """
    start_obj = c.pyapi.object_getattr_string(obj, "start")
    end_obj = c.pyapi.object_getattr_string(obj, "end")
    interval = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    interval.start = c.pyapi.float_as_double(start_obj)
    interval.end = c.pyapi.float_as_double(end_obj)
    c.pyapi.decref(start_obj)
    c.pyapi.decref(end_obj)
    is_error = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(interval._getvalue(), is_error=is_error)


@box(IntervalType)
def box_interval(typ, val, c):
    """
    Convert a native interval structure to an Interval object.
    """
    interval = cgutils.create_struct_proxy(
        typ)(c.context, c.builder, value=val)
    start_obj = c.pyapi.float_from_double(interval.start)
    end_obj = c.pyapi.float_from_double(interval.end)
    class_obj = c.pyapi.unserialize(c.pyapi.serialize_object(Interval))
    res = c.pyapi.call_function_objargs(class_obj, (start_obj, end_obj))
    c.pyapi.decref(start_obj)
    c.pyapi.decref(end_obj)
    c.pyapi.decref(class_obj)
    return res


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

@jit(nopython=True)
def pythagorean_triples_in_interval_numba(i):
    return i.pythagorean_triples_in_interval()

def pythagorean_triples_in_interval_py(i):
    triples = []
    for a in range(int(i.start), int(i.end)):
        for b in range(a, int(i.end)):
            c = (a ** 2 + b ** 2) ** 0.5
            if inside_interval_py(i, c):
                triples.append((a, b, c))
    return triples


if __name__ == '__main__':
    i = Interval(10, 1000)
    st = time.time()
    for _ in range(10):
        pythagorean_triples_in_interval(i)
    print(time.time() - st)

    # st = time.time()
    # for _ in range(10):
    #     pythagorean_triples_in_interval_numba(i)
    # print(time.time() - st)

    st = time.time()
    for _ in range(10):
        pythagorean_triples_in_interval_py(i)
    print(time.time() - st)
