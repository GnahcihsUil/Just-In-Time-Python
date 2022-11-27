import numpy as np
import copy
import matplotlib.pyplot as plt
from input import const_input, ramp_input

'''
LIF neuron model: (dV/dt) = - (V - (V_rest + stim * R)) / tau
'''

class LIF:
    '''
    LIF neuron model: (dV/dt) = - (V - (V_rest + stim * R)) / tau
    '''
    def __init__(self, V_rest = -70., V_reset = -70., V_th = -55., R = 1., tau = 10.):
        self.V_rest = V_rest
        self.V_reset = V_reset
        self.V_th = V_th
        self.R = R
        self.tau = tau

def LIF_simulate():
    # LIF params
    V_rest = -70.   # resting potential in mV
    V_reset = -70.  # reset potential in mV
    V_th = -55.     # spike threshold potential in mV
    R = 1.          # membrane resistance in ?
    tau = 10.       # time const in ms

    # record value in list
    simu_time = 100 # simulation time in ms
    ts = 0.01       # time step in ms

    epochs = int(simu_time // ts + 1)
    stim_list = const_input(20., 100., ts)
    #stim_list = np.array([20.] * 1000 + [0.] * 9000)
    # list of input, change with different input waveform
    neu = LIF(V_rest = V_rest, V_reset = V_reset, V_th = V_th, R = R, tau = tau)

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
        # t += ts
        # return t, V, spike, last_spike_t

        # _, V_new, spike_new, last_spike_t_new = neu.simulate(
        #     t, V, spike, last_spike_t, stim_list[epoch], ts
        # )
        t_list.append(t)
        V_list.append(V)
        spike_list.append(spike)
        last_spike_t_list.append(last_spike_t)

    # fig, axs = plt.subplots(2, 1)
    # axs[0].plot(t_list, stim_list, label = f"input = 20")
    # axs[1].plot(t_list, V_list, label = 'V1')
    # plt.show()

LIF_simulate()

