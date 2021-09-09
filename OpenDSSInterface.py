import win32com.client
# import dss    # pip install dss_python
import pandas as pd
import math
import numpy as np

class DSS:
    # Define the class for OpenDSS
    def __init__(self):
        self.engine = win32com.client.Dispatch("OpenDSSEngine.DSS")
        self.text = self.engine.Text                # enable control by text
        self.text.Command = "clear"                 # following text are initializing
        self.text.Command = "New Circuit.Simple"
        self.circuit = self.engine.ActiveCircuit    # build new circuit 
        print("OpenDSS Engine started successfully")

    def Powersystemcalculation(self, Sim_timestep, EWH_house_load_onestep):
        # input: simulation timestep, power of EWH and other house load at each time step
        # output: total power, voltage at each bus
        ## sum the load under same load
        Loadsupdate = EWH_house_load_onestep.groupby("Node name").sum()   # sum up the power at each node as input
        for casename, values in Loadsupdate.iterrows():  # deal with the data from each house
            self.text.Command = 'Edit Load.' + casename + ' kW=' + str(values["EWH power [kW]"]+values["Other load [kW]"])
            self.text.Command = 'Edit Load.' + casename + ' PF=' + str(0.95)
        ## solve the power system after getting the power results 
        self.text.Command = 'Solve mode=snap'
        self.text.Command = 'sample'
        ### retrive powers
        ActiveP = -self.circuit.TotalPower[0]
        ReactiveP = -self.circuit.TotalPower[1]
        Poweroutput_df = pd.Series({"Active power [kW]":ActiveP,"Reactive power [kW]":ReactiveP}, name = Sim_timestep)   
        ### retrive voltages
        Busnames = self.circuit.AllBusNames
        Volbus_df = pd.Series(dtype=object)   # recorder of bus voltage
        for bus in Busnames:
            self.circuit.SetActiveBus(bus)
            BusnodeNum = self.circuit.ActiveBus.NumNodes   # how many loads are in this bus
            onebusVol = self.circuit.ActiveBus.puVmagAngle # voltages at this bus, (Mag, Angle)
            for PhaseNum in range(1,BusnodeNum+1,1):
                Volname = f'{bus}_p{PhaseNum} [p.u.]'  # the bus name with phase number
                VpuMag_oneph = onebusVol[(PhaseNum-1)*2]    # take the voltage magnitude of one phase
                VpuMag_oneph_df = pd.Series({Volname:VpuMag_oneph}, name=Sim_timestep)
                Volbus_df = pd.Series.add(Volbus_df, VpuMag_oneph_df, fill_value=0)
        ### wrap the output data
        Powersystemresult_onestep = pd.Series.add(Poweroutput_df, Volbus_df, fill_value=0)
        return Powersystemresult_onestep
        
    
    
    
    #     # Retrieve voltages
    # Busnames = d.circuit.AllBusNames
    # VMagPhA = []
    # for i in range(len(Busnames)):
    #     d.circuit.SetActiveBus(Busnames[i])
    #     Voltages = d.circuit.ActiveBus.puVmagAngle
    #     VMagPhA.append(Voltages[0])
    # #Retrieve Line Currents
    # ElemNames = d.circuit.AllElementNames
    # ElemNames = [x for x in ElemNames if "Line" in x or "Vsource" in x or "Trans" in x]
    # AMagPhA = []
    # for i in range(len(ElemNames)):
    #     d.circuit.SetActiveElement(ElemNames[i])
    #     Currents = d.circuit.ActiveCktElement.CurrentsMagAng
    #     AMagPhA.append(Currents[0])
    
# if __name__=="__main__":
#     DSS123bus = DSS()   
#     OpenDSS_mater_file = r'./CommunityOptimalcontrol/DSSmodels/123Bus/IEEE123Master.DSS'
#     DSS123bus.text.Command = "redirect " + OpenDSS_mater_file
#     DSS123bus.text.Command = 'Solve mode=snap'
    # DSSLoadsCOM = DSS123bus.circuit.Loads
    # Loadnames = DSSLoadsCOM.AllNames
    # Busnames = DSS123bus.circuit.AllBusNames
    # a = DSS123bus.circuit.AllBusVolts
    # b = DSS123bus.circuit.AllBusNames 
    # c= DSS123bus.circuit.AllNodeNames
    # d = DSS123bus.circuit.TotalPower


    # AllElement = DSS123bus.circuit.AllElementNames
    # OP = DSS123bus.Powersystemcalculation(0,House_power_all_onestep)
    # print("DONE!")