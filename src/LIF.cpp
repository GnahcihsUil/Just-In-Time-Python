
class LIF {
public:
  LIF(float V_rest, float V_reset, float V_th, float R, float tau) :
    V_rest(V_rest), V_reset(V_reset), V_th(V_th), R(R), tau(tau) {
  };
  float V_rest;
  float V_reset;
  float V_th;
  float R;
  float tau;
};

extern "C" void LIF_simulate() {
  // LIF params
  float V_rest = -70.;   // resting potential in mV
  float V_reset = -70.;  // reset potential in mV
  float V_th = -55.;     // spike threshold potential in mV
  float R = 1.;          // membrane resistance in ?
  float tau = 10.;       // time const in ms

  // record value in list
  float simu_time = 1000; // simulation time in ms
  float ts = 0.01;       // time step in ms

  int epochs = int(simu_time / ts + 1);
  float stim_list[epochs];
  for (int i = 0; i < epochs; i++) {
    stim_list[i] = 20.0;
  }

  //stim_list = np.array([20.] * 1000 + [0.] * 9000)
  // list of input, change with different input waveform
  LIF neu = LIF(V_rest = V_rest, V_reset = V_reset, V_th = V_th, R = R, tau = tau);

  float t_list[epochs];
  float V_list[epochs];
  float spike_list[epochs];
  float last_spike_t_list[epochs];

  float t = 0.;
  float V = -70.;
  float spike = 0.;
  float last_spike_t = -1e6;
  for (int epoch = 0; epoch < epochs; epoch++) {
    t = t + ts;
    spike = 0.;
    float dvdt = -((V - (neu.V_rest + stim_list[epoch] * neu.R)) / neu.tau);
    V = V + ts * dvdt;
    if (V >= neu.V_th) {
      V = neu.V_reset;
      spike = 1.;
      last_spike_t = t;
    }
    t_list[epoch] = t;
    V_list[epoch] = V;
    spike_list[epoch] = spike;
    last_spike_t_list[epoch] = last_spike_t;
  }
}
