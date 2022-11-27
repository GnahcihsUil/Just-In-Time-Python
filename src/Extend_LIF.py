from input import const_input
import time
import ctypes
from numba.extending import box
from numba.extending import unbox, NativeValue
from numba.core import cgutils
from numba.extending import lower_builtin
import numpy as np
from LIF import LIF
from numba import types
from numba.extending import typeof_impl, as_numba_type, type_callable, models, register_model, make_attribute_wrapper
from numba import jit


class LIFType(types.Type):
    def __init__(self):
        super(LIFType, self).__init__(name='LIF')


lif_type = LIFType()

# This is the function that Numba will call to get the type of an LIF
# infer numba type of python object
# runtime


@typeof_impl.register(LIF)
def typeof_index(val, c):
    return lif_type


# infer the Numba type of Python types
# compile time
as_numba_type.register(LIF, lif_type)


@type_callable(LIF)
def type_lif(context):
    def typer(V_rest, tau, R, V_th, V_reset):
        if isinstance(V_rest, types.Float) and isinstance(tau, types.Float) and isinstance(R, types.Float) and isinstance(V_th, types.Float) and isinstance(V_reset, types.Float):
            return lif_type
    return typer


@register_model(LIFType)
class LIFModel(models.StructModel):
    def __init__(self, dmm, fe_type):
        members = [
            ('V_rest', types.float64),
            ('tau', types.float64),
            ('R', types.float64),
            ('V_th', types.float64),
            ('V_reset', types.float64),
        ]
        models.StructModel.__init__(self, dmm, fe_type, members)


make_attribute_wrapper(LIFType, 'V_rest', 'V_rest')
make_attribute_wrapper(LIFType, 'tau', 'tau')
make_attribute_wrapper(LIFType, 'R', 'R')
make_attribute_wrapper(LIFType, 'V_th', 'V_th')
make_attribute_wrapper(LIFType, 'V_reset', 'V_reset')


@lower_builtin(LIF, types.Float, types.Float, types.Float, types.Float, types.Float)
def impl_lif(context, builder, sig, args):
    typ = sig.return_type
    V_rest, tau, R, V_th, V_reset = args
    lif = cgutils.create_struct_proxy(typ)(context, builder)
    lif.V_rest = V_rest
    lif.tau = tau
    lif.R = R
    lif.V_th = V_th
    lif.V_reset = V_reset
    return lif._getvalue()


@unbox(LIFType)
def unbox_lif(typ, obj, c):
    lif = cgutils.create_struct_proxy(typ)(c.context, c.builder)
    lif.V_rest = c.pyapi.object_getattr_string(obj, "V_rest")
    lif.tau = c.pyapi.object_getattr_string(obj, "tau")
    lif.R = c.pyapi.object_getattr_string(obj, "R")
    lif.V_th = c.pyapi.object_getattr_string(obj, "V_th")
    lif.V_reset = c.pyapi.object_getattr_string(obj, "V_reset")
    is_error = cgutils.is_not_null(c.builder, c.pyapi.err_occurred())
    return NativeValue(lif._getvalue(), is_error=is_error)


@box(LIFType)
def box_lif(typ, val, c):
    lif = cgutils.create_struct_proxy(typ)(c.context, c.builder, value=val)
    lif_obj = c.pyapi.unserialize(c.pyapi.serialize_object(LIF))
    c.pyapi.object_setattr_string(lif_obj, "V_rest", lif.V_rest)
    c.pyapi.object_setattr_string(lif_obj, "tau", lif.tau)
    c.pyapi.object_setattr_string(lif_obj, "R", lif.R)
    c.pyapi.object_setattr_string(lif_obj, "V_th", lif.V_th)
    c.pyapi.object_setattr_string(lif_obj, "V_reset", lif.V_reset)
    return lif_obj


@jit(nopython=True)
def LIF_simulate():
    # LIF params
    V_rest = -70.   # resting potential in mV
    V_reset = -70.  # reset potential in mV
    V_th = -55.     # spike threshold potential in mV
    R = 1.          # membrane resistance in ?
    tau = 10.       # time const in ms

    # record value in list
    simu_time = 1000  # simulation time in ms
    ts = 0.01       # time step in ms

    epochs = int(simu_time // ts + 1)
    stim_list = np.array([20.0] * epochs)

    #stim_list = np.array([20.] * 1000 + [0.] * 9000)
    # list of input, change with different input waveform
    neu = LIF(V_rest=V_rest, V_reset=V_reset, V_th=V_th, R=R, tau=tau)

    t_list = []
    V_list = []
    spike_list = []
    last_spike_t_list = []

    t = 0.
    V = -70.
    spike = 0.
    last_spike_t = -1e6
    for epoch in range(epochs):
        t = t + ts
        spike = 0.
        dvdt = - ((V - (neu.V_rest + stim_list[epoch] * neu.R)) / neu.tau)
        V = V + ts * dvdt
        if V >= neu.V_th:
            V = neu.V_reset
            spike = 1.
            last_spike_t = t
        t_list.append(t)
        V_list.append(V)
        spike_list.append(spike)
        last_spike_t_list.append(last_spike_t)


def LIF_simulate_py():
    # LIF params
    V_rest = -70.   # resting potential in mV
    V_reset = -70.  # reset potential in mV
    V_th = -55.     # spike threshold potential in mV
    R = 1.          # membrane resistance in ?
    tau = 10.       # time const in ms

    # record value in list
    simu_time = 1000  # simulation time in ms
    ts = 0.01       # time step in ms

    epochs = int(simu_time // ts + 1)
    stim_list = np.array([20.0] * epochs)

    #stim_list = np.array([20.] * 1000 + [0.] * 9000)
    # list of input, change with different input waveform
    neu = LIF(V_rest=V_rest, V_reset=V_reset, V_th=V_th, R=R, tau=tau)

    t_list = []
    V_list = []
    spike_list = []
    last_spike_t_list = []

    t = 0.
    V = -70.
    spike = 0.
    last_spike_t = -1e6
    for epoch in range(epochs):
        t = t + ts
        spike = 0.
        dvdt = - ((V - (neu.V_rest + stim_list[epoch] * neu.R)) / neu.tau)
        V = V + ts * dvdt
        if V >= neu.V_th:
            V = neu.V_reset
            spike = 1.
            last_spike_t = t
        t_list.append(t)
        V_list.append(V)
        spike_list.append(spike)
        last_spike_t_list.append(last_spike_t)


class Simulate:
    def LIF_simulate(self):
        raise NotImplementedError

    def __call__(self):
        st = time.time()
        n = 100
        for _ in range(n):
            self.LIF_simulate()
        print(f"{type(self).__name__} took {(time.time() - st)/n}")


class SimulateNumba(Simulate):
    def LIF_simulate(self):
        return LIF_simulate()


class SimulatePython(Simulate):
    def LIF_simulate(self):
        return LIF_simulate_py()


class SimulateCpp(Simulate):
    def __init__(self) -> None:
        lib = ctypes.cdll.LoadLibrary("./src/LIF_gcc_o3.so")
        fun = lib.LIF_simulate
        fun.restype = None
        fun.argtypes = None
        self.fun = fun

    def LIF_simulate(self):
        self.fun()

    # def LIF_simulate(self):
    #     return LIF_simulate_cpp()


if __name__ == '__main__':
    simulate_types = [SimulateNumba(), SimulatePython(), SimulateCpp()]
    for simulate_type in simulate_types:
        simulate_type()
        
    st = time.time()
    for i in range(100):
        LIF_simulate()
    print(time.time() - st)

    st = time.time()
    for i in range(100):
        LIF_simulate_py()
    print(time.time() - st)
    # LIF_simulate()
