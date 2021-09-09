import pickle
import numpy as np
from Constantvalues import gallontom3, theta_max, theta_min_resistive, resolution

# load the saved list
with open('Outputs/results_2021_0908_1654.p', 'rb') as config_dictionary_file:
    Loadedresults = pickle.load(config_dictionary_file)
# seperate the two results
Initialize_total = Loadedresults['Initialize_total']
Resultsummary = Loadedresults['Resultsummary']
DRsignal_allstep = Loadedresults['DRsignals']
    

# power system
P_kW = Resultsummary['Active power [kW]']
P_kva = Resultsummary['Reactive power [kW]']
# single EWH    
a1=Initialize_total['Obj']['EWH_0'].theta_record
a2=Initialize_total['Obj']['EWH_0'].DRsignal_record
a3=Initialize_total['Obj']['EWH_0'].EWHPower_record
a4=Initialize_total['Obj']['EWH_0'].Energytake_cumulative_record
a5=Initialize_total['Obj']['EWH_0'].Houseotherload_record
a6=Initialize_total['Obj']['EWH_0'].HWDoutlet_record



b=Initialize_total['Obj']['EWH_0']
## example results for individual EWHs
# EWHobj = EWH_obj  # which EWH
# TankwaterTemp_record = EWHobj.theta_record
# Energytake_cumulative_recor=EWHobj.Energytake_cumulative_record
# S_record= EWHobj.S_record
# EWHPower_record= EWHobj.EWHPower_record
# DRsignal_record= EWH_obj.DRsignal_record
# Otherhouseload = EWH_obj.Houseotherload_record
