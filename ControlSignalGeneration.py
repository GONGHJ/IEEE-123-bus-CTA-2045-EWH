# input: time step
# output: control signal for all EWHs for one time step
from Constantvalues import DRsignals_names,resolution # generate the DR signal
# import pandas as pd

def Controlsignal(timestep):
    DRsignals= DRsignals_names[0]    # normal operation
    if timestep >=12/resolution and timestep <= 16/resolution:
        DRsignals = DRsignals_names[2] # load up
        print(DRsignals_names[2] + str(timestep*resolution ))
    if timestep >=8/resolution and timestep <= 10/resolution:
        DRsignals = DRsignals_names[1] # shed event
        print(DRsignals_names[1] + str(timestep*resolution ))
    if timestep >=17/resolution and timestep <= 19/resolution:
        DRsignals = DRsignals_names[1] # shed event
        print(DRsignals_names[1] + str(timestep*resolution ))
    return  DRsignals
    # return DRsignals_names[0]