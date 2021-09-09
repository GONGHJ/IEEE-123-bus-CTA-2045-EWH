# Load the house load at each time stap. Input: simulation timestep, House ID; output: house load [kW] at the this minute
## important: original data is 15-minute but the I/O of this function should be 1-minute
from Initialize_forsimulationonly import  Fisttimepoint, conn
import datetime
import pandas as pd
import pyodbc 

def Houselodad_read(timestap, HouseId):
    minute_increamental = int(timestap/15)*15     # the minute changes every 5 simulation time stpe
    minutes_added = datetime.timedelta(minutes = minute_increamental) # convert the 5-minute to datetime format
    timeforsql = Fisttimepoint + minutes_added   # generate the SQL recognized data form
    sql_Houseload = f'SELECT kWh  FROM Selected_house_dailyprofile WHERE [House ID]={HouseId} AND Time=\'{timeforsql}\''   # SQL string
    HouseloadkWh_df= pd.read_sql(sql_Houseload,  conn)  # read data from SQL database
    HouseloadkW_value = HouseloadkWh_df.iloc[0]* 60 / 15  # the original data has resolutio of 15-minute
    return HouseloadkW_value[0]     # just return the single value


# if __name__=="__main__":
#     a = Houselodad_read(1441, values["House ID"])
#     print(a)