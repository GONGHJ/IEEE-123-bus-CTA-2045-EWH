# library
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
from multiprocessing import Process, Queue 
# self defined class/function
from Initialize_forsimulationonly import SelectedProfiles, Initialize_total, Totaltimestep, DSS123bus, Resultsummary, DRsignal_allstep  # initialize
from EWH_class import EWH # EWH model
from Constantvalues import DRsignals_names # generate the DR signal
from Readhouseload import Houselodad_read # read other house load
from ControlSignalGeneration import Controlsignal

SimulationStartTime = datetime.now() 
print("Simulation starts at: " + SimulationStartTime.strftime("%H:%M:%S")) 
for i in range(0,Totaltimestep):
# for i in range(0,2):
    # initialize temporary variables to collect EWH results, for power system solver and for control, only need for each time step
    House_power_all_onestep = pd.DataFrame(columns=("EWH power [kW]","Other load [kW]","Node name"))   # record the house load for each residence at each time step
    TankwaterTemp_all_onestep =pd.DataFrame(columns=("Tank temperature [C]",))
    DRsignal_onestep = Controlsignal(i)           # DR signal for selected EWH at given timestep
    print(f'Now at time step: {i}.\n')
    for casename, values in Initialize_total.iterrows():  # run each EWH and collect the results
        WaterflowatFixture_onestep = np.array(SelectedProfiles[values["HWDprofile"]])[i,]   # the hot water flow for selected profile at given time step
        HouseotherkW = Houselodad_read(i, values["House ID"]) # load the other house load from the database.       
        # execute the EWH obj
        EWH_obj = values["Obj"]
        TankwaterTemp_new, Energytake_cumulative_new, S_new, EWHpower_new =EWH_obj.TankWaterTempCalculation(WaterflowatFixture_onestep, DRsignal_onestep, HouseotherkW) 
        # record the individual result for this time step
        Newcase_power = pd.Series({"EWH power [kW]": EWHpower_new, "Other load [kW]" : HouseotherkW, "Node name": values["Node name"]}, name = casename)   
        # Newcase_temperature = pd.Series({"Tank temperature [C]": TankwaterTemp_new}, name = casename)   
        Newcase_temperature = pd.Series({"Tank temperature [C]": TankwaterTemp_new}, name = casename)   
        # record each EWH output
        House_power_all_onestep= House_power_all_onestep.append(Newcase_power)   # EWH name, EWH power, other load power
        TankwaterTemp_all_onestep= TankwaterTemp_all_onestep.append(Newcase_temperature) # EWH name, Tank tamperature  
    ## solve the power system, save the results
    DRsignal_allstep.append(DRsignal_onestep)
    PSresult_onestep = DSS123bus.Powersystemcalculation(i, House_power_all_onestep)      
    Resultsummary=Resultsummary.append(PSresult_onestep, ignore_index=True) # record the power system results
    # check why negative reactive power

SimulationEndTime = datetime.now()
print("Simulation ends at: "+ SimulationEndTime.strftime("%H:%M:%S"))
print("Total simulation time: " + str(SimulationEndTime - SimulationStartTime)) 
# save the data
outputfilename = 'Outputs/results_' + SimulationEndTime.strftime("%Y_%m%d_%H%M") + '.p'  # location
Outputforsave = {'Initialize_total':Initialize_total,'Resultsummary':Resultsummary,'DRsignals':DRsignal_allstep}
with open(outputfilename, "wb" ) as save_results:
    pickle.dump(Outputforsave, save_results)

