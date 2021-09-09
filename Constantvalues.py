#### put the constant values here, when change is needed, change it here
ruo = 993  # density of water: kg/m3
c_p = 4179  # J/kg C
gallontom3 = 0.00378541   # convert gallon to m^3
jouletokWh = 2.77778e-7   # convert joule to kWh
## Energy take values: does not change, set by CTA-2045
EnergyTakeCap_min_resistive_normal = 0         # energy take capacity for normal operation: Wh
EnergyTakeCap_max_resistive_shed = 2250    # energy take capacity for shed event: Wh
# EnergyTakeCap_max_resistive_shed = 7000    # energy take capacity for shed event: Wh. ECCE2021 digesst value
EnergyTakeCap_min_resistive_shed = 1800    # energy take capacity for shed event: Wh
EnergyTakeCap_max_resistive_load = 300     # energy take capacity for load event: Wh
EnergyTakeCap_min_resistive_load = 0    #  energy take capacity for load event: Wh. ECCE2021 digesst value
# signal names
DRsignals_names = ['Normal_Operation','Shed','LoadUp']
## basic simulation settings, normally do not change
resolution = 1/60           # 1 min
theta_in = 22         # room temperature, unit: C     
theta_wco = 10        # cold water temperature, unit: C
theta_Ini = (130-32)*5/9             # Initial water temperatur in the tank
theta_max = (135-32)*5/9            # maximum temperature 
theta_min_HPEW = (125-32)*5/9;           # lower than 125F, HPWH on
theta_min_resistive = (115-32)*5/9       # lower than 110F, resistive element kicks in
theta_min = theta_min_resistive 
# addtional source:
EndUseTemp_F = [95.0000,104.6000,78.2000,104.6000,125.0000]  # end use temperature at fixtures unit: F
EndUseTemp  = [(x-32)*5/9 for x in EndUseTemp_F] # end use temperature unit: C
