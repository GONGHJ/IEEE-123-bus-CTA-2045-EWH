##### to initialize the simulation, load water profiles in advance, create EWH objectives and initialize EWHs
# import the constant values
from Constantvalues import gallontom3, theta_max, theta_min_resistive, resolution
# import the library
import numpy as np
import pandas as pd
import random 
import pyodbc 
import datetime
import math
import time
import pickle
# import self defined function
from EWH_class import EWH
from OpenDSSInterface import DSS

# load the initlized(randomized) inputs. Keep them the same to compare with the the control case
with open('Randomeseeds.p', 'rb') as rdseeds:
    InitializedInputs = pickle.load(rdseeds)
HouseID_selected = InitializedInputs['HouseID_selected']
TankwaterTemp_ini_total = InitializedInputs['TankwaterTemp_ini_total']
Energytake_ini_total= InitializedInputs['Energytake_ini_total']
Profilenames = InitializedInputs['Profilenames']
DSSnodeforhouse = InitializedInputs['DSSnodeforhouse']    
SelectedProfiles = InitializedInputs['SelectedProfiles']
# generate new 'Initialize_total'. All the Objectives for EWH should be redefined
Initialize_total = pd.DataFrame(columns=("Obj", "HWDprofile", "House ID", "Node name"))
Initialize_total = pd.DataFrame()
casenumber = 0
for casename, values in HouseID_selected.iterrows():  # run each EWH and collect the results
     # create new objective for EWH, initialize the obj
    newObj = EWH(f'EWH_{casenumber}')  
    newObj.theta_record = [TankwaterTemp_ini_total[casenumber]]
    newObj.Energytake_cumulative_record = [Energytake_ini_total[casenumber]]
    # collect new cases
    Newcase = pd.Series({'House ID':values["House ID"], 'HWDprofile':Profilenames[casenumber],'Obj':newObj, 'Node name': DSSnodeforhouse[casenumber]}, name = f'EWH_{casenumber}')     
    Initialize_total= Initialize_total.append(Newcase)   
    casenumber+=1
#=============================== Initialize openDSS ===============================
DSS123bus = DSS()   
OpenDSS_mater_file = r'./CommunityOptimalcontrol/DSSmodels/123Bus/IEEE123Master.DSS'
DSS123bus.text.Command = "Redirect " + OpenDSS_mater_file
DSS123bus.text.Command = 'Solve mode=snap'    
# ========================= read house load from the databased =====================
## connect to the SQL database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=COE4738\SQLEXPRESS01;'
                      'Database=GKPBsummer;'
                      'Trusted_Connection=yes;')
sql_Timestamp = 'SELECT DISTINCT(Time)  FROM Selected_house_dailyprofile ORDER BY Time ASC'   # SQL string
Timestamp_df= pd.read_sql(sql_Timestamp,  conn)  # read data from SQL database
Fisttimepoint = Timestamp_df["Time"][0]    # this is used to generate the every 15-minute timestamp
# ======================================== other initialization== ======================
Totaltimestep = int(24/resolution)
DRsignal_allstep =[]
Resultsummary = pd.DataFrame()