from Interval import Interval
from numba import types

class IntervalType(types.Type):
    def __init__(self):
        super(IntervalType, self).__init__(name='Interval')

interval_type = IntervalType()