import pickle
import numpy as np
import pandas as pd
from Constantvalues import gallontom3, theta_max, theta_min_resistive, resolution, DRsignals_names

# load the results: uncontrolled
with open('results_uncontrol.p', 'rb') as config_dictionary_file:
    Loadedresults_uncontrolled = pickle.load(config_dictionary_file)
    # seperate the two results
Initialize_total_uncontrolled = Loadedresults_uncontrolled['Initialize_total']
Resultsummary_uncontrolled = Loadedresults_uncontrolled['Resultsummary']
    # load the results: controlled
with open('results_MaximumLoadup.p', 'rb') as config_dictionary_file:
    Loadedresults_controlled = pickle.load(config_dictionary_file)
# seperate the two results
Initialize_total_controlled = Loadedresults_controlled['Initialize_total']
Resultsummary_controlled = Loadedresults_controlled['Resultsummary']
DRsignal_allstep_controlled = Loadedresults_controlled['DRsignals']
# DR signal time
Shedhour1 = [7,10]
Shedhour2 = [17,19]
Loaduphour1 = [6,7]
Loaduphour2 = [11,16]

# plotting parts
# reset all plot settings
import matplotlib as mpl
import matplotlib.pyplot as plt
# from mpl_toolkits.axes_grid1 import make_axes_locatable
mpl.style.use('classic')
# define plots settings
FigureWidth=3.3 #inches; this is used to control the figure width
Proportion=0.62
AxisLineWidth=1.3
LableFontsize= 8
Linewidth = 2
mpl.rcParams['xtick.major.size'] = Linewidth
mpl.rcParams['ytick.major.size'] = Linewidth
mpl.rcParams['axes.labelsize'] = LableFontsize
mpl.rcParams['xtick.labelsize'] = LableFontsize
mpl.rcParams['ytick.labelsize'] = LableFontsize
plt.rcParams["figure.figsize"] = (FigureWidth,FigureWidth*Proportion)
#  ===========================================  Figure 1: boxplot for water temperatures===============================
## tank temperature: uncontrolled
EWHtemp_uncontrolled = pd.DataFrame()
for casename, values in Initialize_total_uncontrolled.iterrows():  # run each EWH and collect the results
    EWHtemp_uncontrolled[casename] = values["Obj"].theta_record
    EWHtemp_uncontrolled_transposed = EWHtemp_uncontrolled.T
## tank temperature: controlled
EWHtemp_controlled = pd.DataFrame()
for casename, values in Initialize_total_controlled.iterrows():  # run each EWH and collect the results
    EWHtemp_controlled[casename] = values["Obj"].theta_record
    EWHtemp_controlled_transposed = EWHtemp_controlled.T
## plotting part
### axis ranges
Sampleperiod = 30  # sample at everying 30 minutes
ylim_C=(30, 80)
ylim_F= (ylim_C[0]*9/5 + 32, ylim_C[1]*9/5 + 32)
Yrange_C = np.arange(30, 81, 10) 
### boxplot formats
boxprops_settings=dict(linestyle='-', linewidth=0.5, color='black')
whiskerprops_settings=dict(color='black',linestyle='dotted', linewidth = 0.3)
capprops_settings=dict(color='black',linewidth=0.3)
flierprops_settings=dict(color='red', markeredgecolor='red', marker = 'o', markersize= 0.5)
medianprops_settings=dict(color='green', linewidth= 1)
# x, y axis settings
fig, (ax1,ax2) = plt.subplots(2,1, sharex=True, sharey = True, figsize=(FigureWidth,FigureWidth*Proportion), constrained_layout=False)
## subplot1
ax1.set(xlim=(0.5, 49.5), ylim=ylim_C)
plt.yticks(Yrange_C)
h1 = ax1.boxplot(EWHtemp_uncontrolled_transposed.loc[:,range(0,1441,Sampleperiod)], notch=True, widths =0.7, 
                 patch_artist=True,boxprops=boxprops_settings,whiskerprops=whiskerprops_settings,
                 capprops=capprops_settings,flierprops=flierprops_settings,medianprops=medianprops_settings)
## subplot2
ax2.set(xlim=(0.2, 49.8), ylim=ylim_C)
plt.yticks(Yrange_C)
h2 = ax2.boxplot(EWHtemp_controlled_transposed.loc[:,range(0,1441,Sampleperiod)], notch=True, widths =0.7, 
                 patch_artist=True,boxprops=boxprops_settings,whiskerprops=whiskerprops_settings,
                 capprops=capprops_settings,flierprops=flierprops_settings,medianprops=medianprops_settings)
# highlight area
plt.axvspan(Shedhour1[0]*2+1,Shedhour1[1]*2+1, color='grey', alpha=0.3)
plt.axvspan(Shedhour2[0]*2+1,Shedhour2[1]*2+1, color='grey', alpha=0.3)
plt.axvspan(Loaduphour1[0]*2+1,Loaduphour1[1]*2+1, color='grey', alpha=0.1)
plt.axvspan(Loaduphour2[0]*2+1,Loaduphour2[1]*2+1, color='grey', alpha=0.1)
### left y label
fig.supylabel('Temperature [C]', fontsize = 9)
### x label
plt.xticks([])  
plt.xlabel('Time [h]')
plt.xticks(np.array(range(1,50,6)), np.array(range(0,25,3)))
## righ y-axis
ax1_righty = ax1.twinx()       # instantiate a second axes that shares the same x-axis
ax1_righty.set_ylim(ylim_F)
plt.yticks(Yrange_C*9/5 + 32)
ax2_righty = ax2.twinx()       # instantiate a second axes that shares the same x-axis
ax2_righty.set_ylim(ylim_F)
plt.yticks(Yrange_C*9/5 + 32)
plt.text(56, 123, 'Temperature [F]',fontsize = 9,rotation=90)
### y label
plt.ylabel('Temperature [C]', color='white')
# # save the plot
Figname = 'Tempboxplot.PNG'
plt.savefig(Figname, dpi=600, bbox_inches='tight')
plt.show()
#  ===========================================  Figure 2: boxplot for Energy take===============================
## Energytake: uncontrolled
EWHEnergytake_uncontrolled = pd.DataFrame()
for casename, values in Initialize_total_uncontrolled.iterrows():  # run each EWH and collect the results
    EWHEnergytake_uncontrolled[casename] = values["Obj"].Energytake_cumulative_record
    EWHEnergytake_uncontrolled_transposed = EWHEnergytake_uncontrolled.T
    EWHEnergytake_uncontrolloedSampled = EWHEnergytake_uncontrolled_transposed.loc[:,range(0,1440,30)]
## Energytake: controlled
EWHEnergytake_controlled = pd.DataFrame()
for casename, values in Initialize_total_controlled.iterrows():  # run each EWH and collect the results
    EWHEnergytake_controlled[casename] = values["Obj"].Energytake_cumulative_record
    EWHEnergytake_controlled_transposed = EWHEnergytake_controlled.T
    EWHEnergytake_controlloedSampled = EWHEnergytake_controlled_transposed.loc[:,range(0,1440,30)]
## plotting part
### axis ranges
Sampleperiod = 30  # sample at everying 30 minutes
ylim_C=(-6, 6)
ylim_F= (ylim_C[0]*9/5 + 32, ylim_C[1]*9/5 + 32)
Yrange_C = np.arange(ylim_C[0], ylim_C[1]+0.1, 2) 
### boxplot formats
boxprops_settings=dict(linestyle='-', linewidth=0.5, color='black')
whiskerprops_settings=dict(color='black',linestyle='dotted', linewidth = 0.3)
capprops_settings=dict(color='black',linewidth=0.3)
flierprops_settings=dict(color='red', markeredgecolor='red', marker = 'o', markersize= 0.5)
medianprops_settings=dict(color='green', linewidth= 1)
# x, y axis settings
fig, (ax1,ax2) = plt.subplots(2,1, sharex=True, sharey = True, figsize=(FigureWidth,FigureWidth*Proportion), constrained_layout=False)
## subplot1
ax1.set(xlim=(0.5, 49.5), ylim=ylim_C)
plt.yticks(Yrange_C)
h1 = ax1.boxplot(EWHEnergytake_uncontrolled_transposed.loc[:,range(0,1441,Sampleperiod)]/1000, notch=True, widths =0.7, 
                 patch_artist=True,boxprops=boxprops_settings,whiskerprops=whiskerprops_settings,
                 capprops=capprops_settings,flierprops=flierprops_settings,medianprops=medianprops_settings)
## subplot2
ax2.set(xlim=(0.2, 49.8), ylim=ylim_C)
plt.yticks(Yrange_C)
h2 = ax2.boxplot(EWHEnergytake_controlled_transposed.loc[:,range(0,1441,Sampleperiod)]/1000, notch=True, widths =0.7, 
                 patch_artist=True,boxprops=boxprops_settings,whiskerprops=whiskerprops_settings,
                 capprops=capprops_settings,flierprops=flierprops_settings,medianprops=medianprops_settings)
# highlight area
plt.axvspan(Shedhour1[0]*2+1,Shedhour1[1]*2+1, color='grey', alpha=0.3)
plt.axvspan(Shedhour2[0]*2+1,Shedhour2[1]*2+1, color='grey', alpha=0.3)
plt.axvspan(Loaduphour1[0]*2+1,Loaduphour1[1]*2+1, color='grey', alpha=0.1)
plt.axvspan(Loaduphour2[0]*2+1,Loaduphour2[1]*2+1, color='grey', alpha=0.1)


### left y label
fig.supylabel('Energy take [kWh]', fontsize = 9)
### x label
plt.xticks([])  
plt.xlabel('Time [h]')
plt.xticks(np.array(range(1,50,6)), np.array(range(0,25,3)))
# # save the plot
Figname = 'Energtakeboxplot.PNG'
plt.savefig(Figname, dpi=600, bbox_inches='tight')
plt.show()
#  ===========================================  Figure 3: boxplot for total house load, including EWH===============================
## House total load: uncontrolled
Housetotal_uncontrolled = pd.DataFrame()
for casename, values in Initialize_total_uncontrolled.iterrows():  # run each EWH and collect the results
    Housetotal_uncontrolled[casename] = values["Obj"].Houseotherload_record + values["Obj"].EWHPower_record 
    Housetotal_uncontrolled_transposed = Housetotal_uncontrolled.T
## House total load: controlled
Housetotal_controlled = pd.DataFrame()
for casename, values in Initialize_total_controlled.iterrows():  # run each EWH and collect the results
    Housetotal_controlled[casename] = values["Obj"].Houseotherload_record + values["Obj"].EWHPower_record 
    Housetotal_controlled_transposed = Housetotal_controlled.T
## plotting part
### axis ranges
Sampleperiod = 30  # sample at everying 30 minutes
ylim_C=(0, 10)
ylim_F= (ylim_C[0]*9/5 + 32, ylim_C[1]*9/5 + 32)
Yrange_C = np.arange(ylim_C[0], ylim_C[1]+0.1, 2) 
### boxplot formats
boxprops_settings=dict(linestyle='-', linewidth=0.5, color='black')
whiskerprops_settings=dict(color='black',linestyle='dotted', linewidth = 0.3)
capprops_settings=dict(color='black',linewidth=0.3)
flierprops_settings=dict(color='red', markeredgecolor='red', marker = 'o', markersize= 0.5)
medianprops_settings=dict(color='green', linewidth= 1)
# x, y axis settings
fig, (ax1,ax2) = plt.subplots(2,1, sharex=True, sharey = True, figsize=(FigureWidth,FigureWidth*Proportion), constrained_layout=False)
## subplot1
ax1.set(xlim=(0.5, 49.5), ylim=ylim_C)
plt.yticks(Yrange_C)
h1 = ax1.boxplot(Housetotal_uncontrolled_transposed.loc[:,range(0,1441,Sampleperiod)], notch=True, widths =0.7, 
                 patch_artist=True,boxprops=boxprops_settings,whiskerprops=whiskerprops_settings,
                 capprops=capprops_settings,flierprops=flierprops_settings,medianprops=medianprops_settings)
## subplot2
ax2.set(xlim=(0.2, 49.8), ylim=ylim_C)
plt.yticks(Yrange_C)
h2 = ax2.boxplot(Housetotal_controlled_transposed.loc[:,range(0,1441,Sampleperiod)], notch=True, widths =0.7, 
                 patch_artist=True,boxprops=boxprops_settings,whiskerprops=whiskerprops_settings,
                 capprops=capprops_settings,flierprops=flierprops_settings,medianprops=medianprops_settings)
# highlight area
plt.axvspan(Shedhour1[0]*2+1,Shedhour1[1]*2+1, color='grey', alpha=0.3)
plt.axvspan(Shedhour2[0]*2+1,Shedhour2[1]*2+1, color='grey', alpha=0.3)
plt.axvspan(Loaduphour1[0]*2+1,Loaduphour1[1]*2+1, color='grey', alpha=0.1)
plt.axvspan(Loaduphour2[0]*2+1,Loaduphour2[1]*2+1, color='grey', alpha=0.1)

### left y label
fig.supylabel('Power [kW]', fontsize = 9)
### x label
plt.xticks([])  
plt.xlabel('Time [h]')
plt.xticks(np.array(range(1,50,6)), np.array(range(0,25,3)))
# # save the plot
Figname = 'Housetotalboxplot.PNG'
plt.savefig(Figname, dpi=600, bbox_inches='tight')
plt.show()
#  ===========================================  Figure 4: boxplot for bus voltages===============================
Sampleperiod = 30  # sample at everying 30 minutes
## bus voltages: uncontrolled
BusVoltages_uncontrolled = Resultsummary_uncontrolled.drop(['Active power [kW]','Reactive power [kW]'],axis=1)
BusVoltages_uncontrolled_transposed = BusVoltages_uncontrolled.T
BusVoltages_uncontrolled_transposed[1440] = BusVoltages_uncontrolled_transposed[1439]
## bus voltages: controlled
BusVoltages_controlled = Resultsummary_controlled.drop(['Active power [kW]','Reactive power [kW]'],axis=1)
BusVoltages_controlled_transposed = BusVoltages_controlled.T
BusVoltages_controlled_transposed[1440]=BusVoltages_controlled_transposed[1439]
## plotting part
### axis ranges
ylim_C=(0.95, 1.05)
ylim_F= (ylim_C[0]*9/5 + 32, ylim_C[1]*9/5 + 32)
Yrange_C = np.arange(ylim_C[0], ylim_C[1]+0.01, 0.05) 
### boxplot formats
boxprops_settings=dict(linestyle='-', linewidth=0.5, color='black')
whiskerprops_settings=dict(color='black',linestyle='dotted', linewidth = 0.3)
capprops_settings=dict(color='black',linewidth=0.3)
flierprops_settings=dict(color='red', markeredgecolor='red', marker = 'o', markersize= 0.5)
medianprops_settings=dict(color='green', linewidth= 1)
# x, y axis settings
fig, (ax1,ax2) = plt.subplots(2,1, sharex=True, sharey = True, figsize=(FigureWidth,FigureWidth*Proportion), constrained_layout=False)
## subplot1
plt.yticks(Yrange_C)
h1 = ax1.boxplot(BusVoltages_uncontrolled_transposed.loc[:,range(0,1441,Sampleperiod)], notch=True, widths =0.7, 
                  patch_artist=True,boxprops=boxprops_settings,whiskerprops=whiskerprops_settings,
                  capprops=capprops_settings,flierprops=flierprops_settings,medianprops=medianprops_settings)
## subplot2
ax2.set(xlim=(0.2, 49.8), ylim=ylim_C)
plt.yticks(Yrange_C)
h2 = ax2.boxplot(BusVoltages_controlled_transposed.loc[:,range(0,1441,Sampleperiod)], notch=True, widths =0.7, 
                  patch_artist=True,boxprops=boxprops_settings,whiskerprops=whiskerprops_settings,
                  capprops=capprops_settings,flierprops=flierprops_settings,medianprops=medianprops_settings)
# highlight area
plt.axvspan(Shedhour1[0]*2+1,Shedhour1[1]*2+1, color='grey', alpha=0.3)
plt.axvspan(Shedhour2[0]*2+1,Shedhour2[1]*2+1, color='grey', alpha=0.3)
plt.axvspan(Loaduphour1[0]*2+1,Loaduphour1[1]*2+1, color='grey', alpha=0.1)
plt.axvspan(Loaduphour2[0]*2+1,Loaduphour2[1]*2+1, color='grey', alpha=0.1)

### left y label
# fig.supylabel('Voltage [p.u.]', fontsize = 9)
plt.text(-9, 1.01, 'Voltage [p.u.]',fontsize = 9,rotation=90)

### x label
# plt.xticks([])  
plt.xlabel('Time [h]')
plt.xticks(np.array(range(1,50,6)), np.array(range(0,25,3)))
### pick the boxes
Comparedhours = [6, 7, 8, 9,10, 11, 12, 13, 14, 15, 16, 17, 18, 19]  # only pick these hours for comparison side by side
# Hex code for each continents color
groups_colors=["black","blue"]
group_hatchs=['\\\\\\\\','------']
# facecolor    
for i in Comparedhours:
    mybox1 = h1['boxes'][int(i*2)]
    mybox1.set_edgecolor(groups_colors[0])
    mybox1.set_hatch(group_hatchs[0])
    mybox2 = h2['boxes'][int(i*2)]
    mybox2.set_edgecolor(groups_colors[1])
    mybox2.set_hatch(group_hatchs[1])

# # save the plot
Figname = 'busvoltagebocplot_allhours.PNG'
plt.savefig(Figname, dpi=600, bbox_inches='tight')
plt.show()
#  ===========================================  Figure 5: boxplot for bus voltages: selected hours===============================
import seaborn as sns
import matplotlib.patches as mpatches

# Sampledhours = [8,9,10,12,13,14,15,16,17,18,19] 
Comparedhours = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]  # only pick these hours for comparison side by side
# Comparedhours = [3, 2, 1, 12, 2.5, 2.1, 2.2, 5]  # only pick these hours for comparison side by side
SampledPoints = [x*60+1 for x in Comparedhours]
## bus voltages: uncontrolled
BusVoltages_uncontrolled = Resultsummary_uncontrolled.drop(['Active power [kW]','Reactive power [kW]'],axis=1)
BusVoltages_uncontrolled_transposed = BusVoltages_uncontrolled.T
BusVoltages_uncontrolled_transposed[-1] = BusVoltages_uncontrolled_transposed[0]
## bus voltages: controlled
BusVoltages_controlled = Resultsummary_controlled.drop(['Active power [kW]','Reactive power [kW]'],axis=1)
BusVoltages_controlled_transposed = BusVoltages_controlled.T
BusVoltages_controlled_transposed[-1] = BusVoltages_controlled_transposed[0]
## plotting part
### axis ranges
ylim_C=(0.95, 1.05)
ylim_F= (ylim_C[0]*9/5 + 32, ylim_C[1]*9/5 + 32)
Yrange_C = np.arange(ylim_C[0], ylim_C[1]+0.01, 0.05) 
### boxplot formats
colors=['white','blue']
boxprops_settings=dict(linestyle='-', linewidth=0.5)
whiskerprops_settings=dict(color='black',linestyle='dotted', linewidth = 0.3)
capprops_settings=dict(color='black',linewidth=0.3)
flierprops_settings=dict(color='red', markeredgecolor='red', marker = 'o', markersize= 0.5)
medianprops_settings=dict(color='green', linewidth= 1.5)
# x, y axis settings
fig, (ax1) = plt.subplots(1,1, sharex=True, sharey = True, figsize=(FigureWidth,FigureWidth*Proportion), constrained_layout=False)

uncontrolled_sampled = BusVoltages_uncontrolled_transposed.loc[:,np.array(SampledPoints)]
uncontrolled_sampled['group']='w/o control'
controlled_sampled = BusVoltages_controlled_transposed.loc[:,np.array(SampledPoints)]
controlled_sampled['group']='w/ control'
Voltages_mixall = pd.concat([uncontrolled_sampled,controlled_sampled]) 
Voltages_melt_forboxplot = pd.melt(Voltages_mixall, id_vars=['group'], value_vars=SampledPoints, var_name='timestep')

h1 = sns.boxplot(x='timestep',y='value',data=Voltages_melt_forboxplot, hue='group', notch=True, 
                 boxprops=boxprops_settings,whiskerprops=whiskerprops_settings,
                  capprops=capprops_settings,flierprops=flierprops_settings,medianprops=medianprops_settings)
# ax1.legend(bbox_to_anchor=(1.0, 0.25), ncol=1, labelspacing=0.2, frameon=False , fontsize=LableFontsize, handlelength=4)
groups = Voltages_melt_forboxplot.timestep.unique().tolist()
# Hex code for each continents color
groups_colors=["black","blue"]
group_hatchs=['\\\\\\\\','------']
groups_dict = dict(zip(groups, groups_colors))
# facecolor    
for i in range(0,len(groups)*2):
    mybox = h1.artists[i]
    mybox.set_facecolor('white')
# edge color    
for i in range(0,len(groups)*2):
    mybox = h1.artists[i]
    mybox.set_edgecolor(groups_dict[groups[i%2]])
# median line
for i in range(0,len(groups)*2):
    mybox = h1.artists[i]
    mybox.set_edgecolor(groups_dict[groups[i%2]])
# add hatches
for i in range(0,len(groups)*2):
    mybox = h1.artists[i]
    mybox.set_hatch(group_hatchs[i%2])
# make the legend
red_patch = mpatches.Patch(facecolor='white',edgecolor=groups_colors[0],hatch=group_hatchs[0], label='w/o control')
blue_patch = mpatches.Patch(facecolor='white',edgecolor=groups_colors[1],hatch=group_hatchs[1], label='w/ control')
plt.legend(handles=[red_patch, blue_patch],bbox_to_anchor=(1.0, 0.25), ncol=1, labelspacing=0.2, frameon=False , fontsize=LableFontsize, handlelength=4)

### left y label
plt.ylabel('Voltage [p.u.]', fontsize = 9)
plt.yticks(Yrange_C)
### x label
# # plt.xticks([])  
plt.xlabel('Selected time [h]')
plt.xticks(np.arange(0,14,1), Comparedhours)
# # # save the plot
Figname = 'busvoltagebocplot_selectedhours.PNG'
plt.savefig(Figname, dpi=600, bbox_inches='tight')
plt.show()
#  ===========================================  Figure 6: barplot for violation times===============================
EWHTemp_uncontrolled = pd.DataFrame()
for casename, values in Initialize_total_uncontrolled.iterrows():  # run each EWH and collect the results
    EWHTemp_uncontrolled[casename] = values["Obj"].theta_record
    EWHTempoutlier_uncontrolled = EWHTemp_uncontrolled< (110-32)*5/9
    EWHTempoutlierName_uncontrolled = EWHTempoutlier_uncontrolled.sum(axis=0)
    EWHoutlierName_uncontrolled = EWHTempoutlierName_uncontrolled[EWHTempoutlierName_uncontrolled>0]
    EWHoutlierNum_uncontrolled=len(EWHoutlierName_uncontrolled)
## Energytake: controlled
EWHTemp_controlled = pd.DataFrame()
for casename, values in Initialize_total_controlled.iterrows():  # run each EWH and collect the results
    EWHTemp_controlled[casename] = values["Obj"].theta_record
    EWHTempoutlier_controlled = EWHTemp_controlled< (110-32)*5/9
    EWHTempoutlierName_controlled = EWHTempoutlier_controlled.sum(axis=0)
    EWHoutlierName_controlled = EWHTempoutlierName_controlled[EWHTempoutlierName_controlled>0]
    EWHoutlierNum_controlled=len(EWHoutlierName_controlled)
## plotting part
### axis ranges
ylim_C=(0.95, 1.05)
ylim_F= (ylim_C[0]*9/5 + 32, ylim_C[1]*9/5 + 32)
Yrange_C = np.arange(ylim_C[0], ylim_C[1]+0.01, 0.05) 
### boxplot formats
colors=['white','blue']
boxprops_settings=dict(linestyle='-', linewidth=0.5)
whiskerprops_settings=dict(color='black',linestyle='dotted', linewidth = 0.3)
capprops_settings=dict(color='black',linewidth=0.3)
flierprops_settings=dict(color='red', markeredgecolor='red', marker = 'o', markersize= 0.5)
medianprops_settings=dict(color='green', linewidth= 1.5)
# x, y axis settings
fig, (ax1) = plt.subplots(1,1, sharex=True, sharey = True, figsize=(FigureWidth,FigureWidth*Proportion), constrained_layout=False)
# x, y axis settings
ax1.set(xlim=(0, 300), ylim=(0, 40))
plt.xlabel('Daily violation minutes')
ax1.set_xticks(np.array(range(0,301,50)))
plt.ylabel('number of EWH')
ax1.set_yticks(np.array(range(0,41,10)))
# h1 = plt.hist(x='timestep',y='value',data=Voltages_melt_forboxplot, hue='group', notch=True, 
#                  boxprops=boxprops_settings,whiskerprops=whiskerprops_settings,
#                   capprops=capprops_settings,flierprops=flierprops_settings,medianprops=medianprops_settings)
groups_colors=["black","blue"]
group_hatchs=['\\\\\\\\','------']
h1 = plt.hist(EWHoutlierName_uncontrolled, bins=30, range=(0,300), alpha=1,facecolor='white',edgecolor=groups_colors[0],hatch=group_hatchs[0], label='w/o control')
h1_data = np.histogram(EWHoutlierName_uncontrolled, bins=30, range=(0,300))
h2 = plt.hist(EWHoutlierName_controlled, bins=30, range=(0,300), alpha=0.3,facecolor='white',edgecolor=groups_colors[1],hatch=group_hatchs[1], label='w/ control')
h2_data = np.histogram(EWHoutlierName_controlled, bins=30, range=(0,300))
# legend
ax1.legend(bbox_to_anchor=(1.0, 0.95), ncol=1, labelspacing=0.5, frameon=False , fontsize=LableFontsize, handlelength=4)
# # # save the plot
Figname = 'TempviolationTime.PNG'
plt.savefig(Figname, dpi=600, bbox_inches='tight')
plt.show()

#  ===========================================  Figure 7: barplot for violation times: energy===============================
EWHEnergytake_uncontrolled = pd.DataFrame()
for casename, values in Initialize_total_uncontrolled.iterrows():  # run each EWH and collect the results
    EWHEnergytake_uncontrolled[casename] = values["Obj"].Energytake_cumulative_record
    EWHEnergytakeoutlier_uncontrolled = EWHEnergytake_uncontrolled > 2300
    EWHEnergytakeoutlierName_uncontrolled = EWHEnergytakeoutlier_uncontrolled.sum(axis=0)
    EWHoutlierName_uncontrolled = EWHEnergytakeoutlierName_uncontrolled[EWHEnergytakeoutlierName_uncontrolled>0]
    EWHoutlierNum_uncontrolled=len(EWHoutlierName_uncontrolled)
## Energytake: controlled
EWHEnergytake_controlled = pd.DataFrame()
for casename, values in Initialize_total_controlled.iterrows():  # run each EWH and collect the results
    EWHEnergytake_controlled[casename] = values["Obj"].Energytake_cumulative_record
    EWHEnergytakeoutlier_controlled = EWHEnergytake_controlled > 2300
    EWHEnergytakeoutlierName_controlled = EWHEnergytakeoutlier_controlled.sum(axis=0)
    EWHoutlierName_controlled = EWHEnergytakeoutlierName_controlled[EWHEnergytakeoutlierName_controlled>0]
    EWHoutlierNum_controlled=len(EWHoutlierName_controlled)
## plotting part
### axis ranges
ylim_C=(0.95, 1.05)
ylim_F= (ylim_C[0]*9/5 + 32, ylim_C[1]*9/5 + 32)
Yrange_C = np.arange(ylim_C[0], ylim_C[1]+0.01, 0.05) 
### boxplot formats
colors=['white','blue']
boxprops_settings=dict(linestyle='-', linewidth=0.5)
whiskerprops_settings=dict(color='black',linestyle='dotted', linewidth = 0.3)
capprops_settings=dict(color='black',linewidth=0.3)
flierprops_settings=dict(color='red', markeredgecolor='red', marker = 'o', markersize= 0.5)
medianprops_settings=dict(color='green', linewidth= 1.5)
# x, y axis settings
fig, (ax1) = plt.subplots(1,1, sharex=True, sharey = True, figsize=(FigureWidth,FigureWidth*Proportion), constrained_layout=False)
# x, y axis settings
ax1.set(xlim=(0, 150), ylim=(0, 60))
plt.xlabel('Daily violation minutes')
ax1.set_xticks(np.array(range(0,151,30)))
plt.ylabel('number of EWH')
ax1.set_yticks(np.array(range(0,61,10)))
# h1 = plt.hist(x='timestep',y='value',data=Voltages_melt_forboxplot, hue='group', notch=True, 
#                  boxprops=boxprops_settings,whiskerprops=whiskerprops_settings,
#                   capprops=capprops_settings,flierprops=flierprops_settings,medianprops=medianprops_settings)
groups_colors=["black","blue"]
group_hatchs=['\\\\\\\\','------']
h1 = plt.hist(EWHoutlierName_uncontrolled, bins=30, range=(0,150), alpha=1,facecolor='white',edgecolor=groups_colors[0],hatch=group_hatchs[0], label='w/o control')
h2 = plt.hist(EWHoutlierName_controlled, bins=30, range=(0,150), alpha=0.3,facecolor='white',edgecolor=groups_colors[1],hatch=group_hatchs[1], label='w/ control')
h1_data = np.histogram(EWHoutlierName_uncontrolled, bins=30, range=(0,150))
Totalmin_nocontrol = sum(h1_data[0])
h2_data = np.histogram(EWHoutlierName_controlled, bins=30, range=(0,150))
Totalmin_control = sum(h2_data[0])

# legend
ax1.legend(bbox_to_anchor=(1.0, 0.95), ncol=1, labelspacing=0.5, frameon=False , fontsize=LableFontsize, handlelength=4)
# # # save the plot
Figname = 'EnergytakeviolationTime.PNG'
plt.savefig(Figname, dpi=600, bbox_inches='tight')
plt.show()