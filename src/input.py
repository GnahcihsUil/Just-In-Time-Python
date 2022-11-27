import numpy as np

def const_input(amp = 0., simuTime = 1000., step = 0.01):
    '''
    Param:
    amp:         amplitude of stimulus
    simuTime:    total time of simulation
    step:        simulation step
    
    Return:
    input:       np.ndarray of constant stimulus amplitude per timestep
    '''
    epoch = int(simuTime // step + 1)
    input = np.array([amp] * epoch)
    return input

def section_input(amp = 0., startTime = 0., endTime = 1000., simuTime = 1000., step = 0.01):
    '''
    Param:
    amp:         amplitude of stimulus
    startTime:   start time of stimulus
    endTime:     end time of stimulus
    simuTime:    total time of simulation
    step:        simulation step
    
    Return:
    input:       np.ndarray of constant stimulus amplitude per timestep
    '''
    epoch = int(simuTime // step + 1)
    startEpoch = int(startTime // step + 1)
    endEpoch = int(endTime // step + 1)
    input = np.array([0] * startEpoch + [amp] * (endEpoch-startEpoch) + [0] * (epoch - endEpoch))
    return input

def biphasic_input(mean = 0., amp = 0., period = 1., 
                   simuTime = 1000., step = 0.01): 
    '''
    Param:
    amp:         amplitude of biphasic stimulus
    period:      period of biphasic_input, 
    simuTime:    total time of simulation
    step:        simulation step
    
    Return:
    input:       np.ndarray of constant stimulus amplitude per timestep
    '''
    epoch = int(simuTime // step + 1)
    change_epoch = int((period/2) // step + 1)
    input = []
    posi = 0
    for i in range(epoch):
        input.append(mean + amp)
        if posi == change_epoch:
            amp = -amp
            posi = 0
        posi += 1
    input = np.array(input)
    return input


def ramp_input(ampSt = 0., ampEnd = 1., 
               simuTime = 1000., step = 0.01):
    '''
    Param:
    ampSt:       Start value of ramping stim
    ampEnd:      End value of ramping stim
    simuTime:    total time of simulation
    step:        simulation step
    
    Return:
    input:       np.ndarray of constant stimulus amplitude per timestep
    '''
    epoch = int(simuTime // step + 1)
    inputList = []
    for i in range(epoch):
        inputList.append(ampSt + (ampEnd - ampSt) / epoch * i)
    input = np.array(inputList)
    return input

def sinuous_input(mean = 0., amp = 1., omega = 1., b = 0.,
                  simuTime = 1000., step = 0.01):
    '''
    Param:
    amp:         Max amplitude of sinuous stim
    omega:       omega of sinuous stim
    b:           b of sinuous stim
    simuTime:    total time of simulation
    step:        simulation step
    
    Return:
    input:       np.ndarray of constant stimulus amplitude per timestep
    '''
    epoch = int(simuTime // step + 1)
    inputList = []
    for i in range(epoch):
        t = i * step
        inputList.append(mean + amp * np.sin(omega * t + b))
    input = np.array(inputList)
    return input
