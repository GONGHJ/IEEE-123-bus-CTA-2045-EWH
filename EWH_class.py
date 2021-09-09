# impot the constant values
from Constantvalues import *

# libraries
import numpy as np

class EWH:
      # define the EWH object, 
    def __init__(self,EWHname):
      self.EWHname = EWHname   # for outsider to self check
      self.internalcounter = 0 # for recording the outputs for each EWH
      ### unchanged value first
      ## constant, never change, values are kept in "Constantvalues.py"
      self.ruo = ruo # density of water: kg/m3
      self.c_p = c_p # J/kg C
      self.gallontom3 = gallontom3   # convert gallon to m^3
      self.jouletokWh = jouletokWh   # convert joule to kWh
      ## Energy take values: does not change, set by CTA-2045
      self.EnergyTakeCap_min_resistive_normal = EnergyTakeCap_min_resistive_normal         # energy take capacity for normal operation: Wh
      self.EnergyTakeCap_max_resistive_shed = EnergyTakeCap_max_resistive_shed    # energy take capacity for shed event: Wh
      # EnergyTakeCap_max_resistive_shed = 7000    # energy take capacity for shed event: Wh. ECCE2021 digesst value
      self.EnergyTakeCap_min_resistive_shed = EnergyTakeCap_min_resistive_shed    # energy take capacity for shed event: Wh
      self.EnergyTakeCap_max_resistive_load = EnergyTakeCap_max_resistive_load     # energy take capacity for load event: Wh
      self.EnergyTakeCap_min_resistive_load = EnergyTakeCap_min_resistive_load    #  energy take capacity for load event: Wh. ECCE2021 digesst value
      ## basic simulation settings, normally do not change
      self.resolution = resolution           # 1 min
      self.theta_in = theta_in  # room temperature, unit: C     
      self.theta_wco = theta_wco        # cold water temperature, unit: C
      self.theta_Ini = theta_Ini             # Initial water temperatur in the tank
      self.theta_max = theta_max            # maximum temperature 
      self.theta_min_HPEW = theta_min_HPEW           # lower than 125F, HPWH on
      self.theta_min_resistive = theta_min_resistive       # lower than 110F, resistive element kicks in
      self.theta_min = self.theta_min_resistive 
      ### values differ by water heaters
      ## EWH characteristics, could change
      self.P_EWH_rated = 4.5  # kW, delivered power
      # R_E = 700     # equivalent resistance for heat pump [600, 800]
      self.R_E = 1500;     # equivalent resistance for resistive EWH [1400,1700]
      self.Volumn = 50        # gallon
      self.C_E = self.Volumn *self.gallontom3 * self.ruo * self.c_p * self.jouletokWh # equivalente thermal capacitance gallon to m3 and J to kWh
      ### simulation initilize, recording outputs
      self.Energytake_cumulative_record = [0]   # initlize the energy take 
      self.theta_record =[self.theta_Ini]   # initialize the temperature in the tank
      self.S_record=[0]  # initialize the On/Off status
      self.EWHPower_record = [0]     
      #### not depend on previous input
      self.Houseotherload_record = [0]
      self.HWDoutlet_record = [0]
      self.DRsignal_record = [DRsignals_names[0]] # initialize the DR signal 
      
    def TankWaterTempCalculation(self, W_t_fixtures, DRsignal, Houseotherload): 
       # update the EWH status, inputs: time step, water flow at fitures (unit: m3), DRsignal, EWH operation status, DR signal, energy take, 
       Q = self.P_EWH_rated             # heat trasfer, in this case only the EWH is included
       # the inputs for this timestep, read old data record
       theta = self.theta_record[self.internalcounter]
       S = self.S_record[self.internalcounter]
       Energytake_cumulative = self.Energytake_cumulative_record[self.internalcounter]
       # calculate the hot water flow at the water tank outlet
       W_t = self.Outletwaterflow(theta, W_t_fixtures)
       # update tank temperature
       theta_new = theta + self.resolution/self.C_E*(S*Q - 1/self.R_E *(theta-self.theta_in)- self.ruo*self.c_p*W_t*(theta-self.theta_wco)*self.jouletokWh/self.resolution)      # calculate the water temperature in the tank
       # calculate and record the energy take
       EnergyTake_oneStep = (theta - theta_new) * self.c_p * self.ruo * self.Volumn * self.gallontom3 * self.jouletokWh * 1000       # calculate the energy take for this time step: Wh
       Energytake_cumulative_new = Energytake_cumulative + EnergyTake_oneStep   # calculate the cumulative energy take
       EnergyTakeCap_min_resistive, EnergyTakeCap_max_resistive = self.Energytakecap(W_t, DRsignal)         # decide the energy take caps for different DR signal
       if Energytake_cumulative_new > EnergyTakeCap_max_resistive and S == 0:   # energy take high, turn on
           S = 1
       elif Energytake_cumulative_new < EnergyTakeCap_min_resistive and S == 1: # energy take low, turn off
           S = 0
       # update and record the new outputs: tank temperature, status, power, energy take, DR signals
       self.Houseotherload_record = np.append(self.Houseotherload_record, Houseotherload)    # this is just for recording the house other load from outside
       self.theta_record= np.append(self.theta_record, theta_new)
       self.S_record = np.append(self.S_record, S)
       self.EWHPower_record = np.append(self.EWHPower_record, Q*S)
       self.Energytake_cumulative_record = np.append(self.Energytake_cumulative_record, Energytake_cumulative_new)
       self.DRsignal_record = np.append(self.DRsignal_record, DRsignal)
       self.HWDoutlet_record = np.append(self.HWDoutlet_record, W_t)
       self.internalcounter+=1   # update the internal counter
       # wrap and output the data   
       return theta_new, Energytake_cumulative_new, S, Q*S  # still have output for power system level. output: water tank temperature, energy take, EWH operation status, EWH power
    
    def Energytakecap(self, W_t, DRsignal):   
        # calculate the energy take cap, inputs: water flow, DR signal
        if DRsignal == 'Normal_Operation':
            EnergyTakeCap_min_resistive = self.EnergyTakeCap_min_resistive_normal  # energy take capacity for normal operation: Wh
            # deide the energy take cap under normal operation according to water flow, unit: gallon
            if W_t/self.gallontom3 > 1:  # water flow: gallon
                EnergyTakeCap_max_resistive = 300 # energy take capacity for normal operation: Wh
            elif W_t/self.gallontom3>0.3: # water flow: gallon
                EnergyTakeCap_max_resistive= 600 # energy take capacity for normal operation: Wh
            else:
                EnergyTakeCap_max_resistive= 900 # energy take capacity for normal operation: Wh                
        elif DRsignal =='Shed':
            EnergyTakeCap_min_resistive = self.EnergyTakeCap_min_resistive_shed   # energy take capacity for shed event: Wh
            EnergyTakeCap_max_resistive = self.EnergyTakeCap_max_resistive_shed   # energy take capacity for shed event: Wh
        elif DRsignal =='LoadUp':
            EnergyTakeCap_min_resistive = self.EnergyTakeCap_min_resistive_load   # energy take capacity for load event: Wh    
            EnergyTakeCap_max_resistive = self.EnergyTakeCap_max_resistive_load   # energy take capacity for load event: Wh           
        else:
            print("DR signal not defined.\n")
        return EnergyTakeCap_min_resistive, EnergyTakeCap_max_resistive #output: min/max energy take as defined by DR signals
    
    def Outletwaterflow(self, theta, W_t_fitures): # input: tank temperature, hot water flow at the fixtures
        # calculate the hot water flow at the EWH tank outlet, inputs: tank temperature, hot water flow at the fixtures, output: flow at EWH outlet: m3
        if theta < min(EndUseTemp):      # Temp does not meet, can't mix cold water
            W_t = sum(W_t_fitures)  # hot water draw as total  
        else:
            W_t =  (np.dot(EndUseTemp, W_t_fitures)-self.theta_wco*sum(W_t_fitures))/(theta-self.theta_wco)  # outlet tank temperature mixed with cold water
        return W_t 
