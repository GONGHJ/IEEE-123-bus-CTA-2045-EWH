##### to initialize the simulation, load water profiles in advance, create EWH objectives and initialize EWHs
#### this will be only run once to generate the random seeds. Later we just read them so we can compare the control results
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


#=======================  which node for the house load to connect ==================================
DSS123bus = DSS()   
OpenDSS_mater_file = r'./CommunityOptimalcontrol/DSSmodels/123Bus/IEEE123Master.DSS'
DSS123bus.text.Command = "Redirect " + OpenDSS_mater_file
DSS123bus.text.Command = 'Solve mode=snap'
DSSLoadsCOM = DSS123bus.circuit.Loads
Loadnames = DSSLoadsCOM.AllNames
DSSLoadsCOM.First   # counting from the first load 
DSSValue_Loads = pd.DataFrame() # empty dataframe to save data
DSSnodeforhouse = list()  # emplty list to save load name and distribution for house connection
for i in range(len(Loadnames)):
    Newload = pd.Series({"Value [kW]": DSSLoadsCOM.kW, "House number": int(math.ceil(DSSLoadsCOM.kW/10))}, name = DSSLoadsCOM.Name)     
    DSSValue_Loads= DSSValue_Loads.append(Newload)
    a = [DSSLoadsCOM.Name] * int(math.ceil(DSSLoadsCOM.kW/10))   # generate the load name list
    DSSnodeforhouse.extend(a)
    DSSLoadsCOM.Next
PSVbase = DSS123bus.circuit.ActiveBus.kVBase # the base voltage [kW]
#================ randomly select the water flow profiles according to the bedroom distribution ========
Profilenames = []     # record all the generated profile names, each element here is input to for the water heater model function
Foldername = r'Python resistive EWH/CBECC-Res-2019_Minute-Flow-Data_v5/'
Daytypes= "D"   # D: weekday, H: holiday, E: weekend
Housenumbers = np.array([0, 7+29, 91, 151, 59, 16]) # bedroom numbers from 0 to 5+. No 0 bedroom so it is combined with 1 bd, but stil need to hold the 0 bd position, total number is defined by the IEEE 123 bus system 
# Housenumbers = np.array([0, 1, 1, 1, 1, 1])
Daynames=[np.random.randint(low=0,high=10,size=Housenumbers[x]) for x in range(len(Housenumbers))] # generate the day numbers as selected day
for BDnumber in range(len(Daynames)):    
    # for a given bedroom number, generate the days for it
    for Day_sequence in range(len(Daynames[BDnumber])):
        #combine the bedroom number, day type and selected schedule day 
        Newprofile = f'{BDnumber}{Daytypes}{Daynames[BDnumber][Day_sequence]}'
        Profilenames.append(Newprofile)
random.shuffle(Profilenames)    # otherwise it is from 0 to 6 bd
#  for checking the distribution of different hot water profiles
# import collections
# counter=collections.Counter(Profilenames)
# print(counter)
## checking ends
# load the profiles csvs, save as list, avoid repeating reading csvs
SelectedProfiles = {}   # record all hot water flow: profile name, and all columns
Profilenames_loading = np.unique(Profilenames)
for Fixturewaterprofile in Profilenames_loading:
    Newprofile_fullname = f'{Foldername}{Fixturewaterprofile}-minutes.csv'
    Fixturewaterflow_raw = pd.read_csv(Newprofile_fullname)          # read the hot water flow from the csv file 
    ApplianceWaterFlow= np.array(Fixturewaterflow_raw.iloc[:,1:6]) * gallontom3     # read the fixutre water flow and convert it to m3
    SelectedProfiles[Fixturewaterprofile] = ApplianceWaterFlow.tolist()             # generate list, use np.array() to bring the columns back
# ========================= read house load from the databased =====================
## connect to the SQL database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=COE4738\SQLEXPRESS01;'
                      'Database=GKPBsummer;'
                      'Trusted_Connection=yes;')
sql_allhouseID = 'SELECT DISTINCT([House ID])  FROM Selected_house_dailyprofile'
HouseIDs = pd.read_sql(sql_allhouseID,  conn)
### select 349 houses
HouseID_selected= HouseIDs.sample(frac=sum(Housenumbers)/len(HouseIDs))  # shuffle and select the house ID sequences
### select the begeining of the time point
sql_Timestamp = 'SELECT DISTINCT(Time)  FROM Selected_house_dailyprofile ORDER BY Time ASC'   # SQL string
Timestamp_df= pd.read_sql(sql_Timestamp,  conn)  # read data from SQL database
Fisttimepoint = Timestamp_df["Time"][0]    # this is used to generate the every 15-minute timestamp
#==================== Initialize the variable for recording the final results: temperature, energy take, power, mark them with case names===================
TankwaterTemp_ini_total = np.random.random_sample((len(Profilenames),1)) * (theta_max - theta_min_resistive) + theta_min_resistive # initialize water temperature in the tank uniform [theta_min_resistive , theta_max]
Energytake_ini_total = np.random.random_sample((len(Profilenames),1)) * (1000 - 0) + 0 # initialize energy take [0, 1000]Wh
#==================== save the randome seeds
Rdseeds = {'HouseID_selected': HouseID_selected, 'TankwaterTemp_ini_total':TankwaterTemp_ini_total, 'SelectedProfiles':SelectedProfiles,
           'Energytake_ini_total':Energytake_ini_total, 'Profilenames':Profilenames,'DSSnodeforhouse':DSSnodeforhouse} # save the random seeds so later we can reload for testing the control
with open('Randomeseeds.p', "wb" ) as save_Rdseeds:
    pickle.dump(Rdseeds, save_Rdseeds)