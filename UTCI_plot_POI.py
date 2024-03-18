import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
# import seaborn as sns
import glob
import os


mpl.use('TkAgg')

mpl.rcParams.update({'font.size': 15})

save_path = os.getcwd().replace('\\', '/') + '/'

# Directory with POI files
poidir = save_path + '/POI_data/'

# List all POIs in poidir
poifiles = glob.glob(poidir + '*.txt')

# Column names for pandas dataframe
poi_columns = ['Year', 'DOY', 'Hour', 'Minute', 'dectime', 'altitude', 'azimuth', 'kdir', 'kdiff', 'kglobal', 'kdown',
               'kup',
               'keast', 'ksouth', 'kwest', 'knorth', 'ldown', 'lup', 'least', 'lsouth', 'lwest', 'lnorth', 'Ta', 'Tg',
               'RH', 'Esky',
               'Tmrt', 'I0', 'CI', 'Shadow', 'SVF_b', 'SVF_bv', 'KsideI', 'PET', 'UTCI', 'CI_Tg', 'CI_TgG', 'KsideD',
               'Lside', 'diffDown', 'Kside']

# Actual dates
labelDict = {'Balbala_open_average_djf': 'Open 2007-01-21',
             'Balbala_open_average_jja': 'Open 1993-07-21',
             'Balbala_open_hot_djf': 'Open 2000-02-21',
             'Balbala_open_hot_jja': 'Open 2015-08-13',
             'Balbala_tree_average_djf': 'Tree 2007-01-21',
             'Balbala_tree_average_jja': 'Tree 1993-07-21',
             'Balbala_tree_hot_djf': 'Tree 2000-02-21',
             'Balbala_tree_hot_jja': 'Tree 2015-08-13'}

# Average current, average future
labelDict_ = {'Balbala_open_average_djf': 'Open present climate',
              'Balbala_open_average_jja': 'Open present climate',
              'Balbala_open_hot_djf': 'Open future climate',
              'Balbala_open_hot_jja': 'Open future climate',
              'Balbala_tree_average_djf': 'Tree present climate',
              'Balbala_tree_average_jja': 'Tree present climate',
              'Balbala_tree_hot_djf': 'Tree future climate',
              'Balbala_tree_hot_jja': 'Tree future climate'}

# ax = plt.subplot(1, 1, 1, projection='polar')
fig = plt.figure(figsize=(12, 6), constrained_layout=True)
gs = fig.add_gridspec(1, 2)

# Add axes, i.e. subplots
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

for poifile in poifiles:
    poi = pd.read_csv(poifile, sep=' ', header=None, skiprows=1, encoding="ISO-8859-1")
    poi.columns = poi_columns
    temp_alt = poi.altitude.to_numpy()
    # temp_hour = poi.Hour.to_numpy()[temp_alt > 0]
    temp_hour = poi.Hour.to_numpy()
    temp_utci = poi.UTCI.to_numpy()[((temp_hour >= 7) & (temp_hour <= 19))]
    temp_hour = temp_hour[((temp_hour >= 7) & (temp_hour <= 19))]
    # temp_utci = poi.UTCI.to_numpy()[temp_alt > 0]
    temp_label = poifile.split('\\')[-1].split('.')[0]
    # Colors, markers and lines for winter
    if 'djf' in temp_label:
        if 'average' in temp_label:
            temp_line = '-'
            temp_mark = 'x'
            if 'tree' in temp_label:
                temp_color = 'green'
            else:
                temp_color = 'magenta'
        else:
            temp_line = ':'
            temp_mark = 'o'
            if 'tree' in temp_label:
                temp_color = 'green'
            else:
                temp_color = 'magenta'
    # Colors, markers and lines for summer
    else:
        if 'average' in temp_label:
            temp_line = '-'
            temp_mark = 'x'
            if 'tree' in temp_label:
                temp_color = 'green'
            else:
                temp_color = 'magenta'
        else:
            temp_line = ':'
            temp_mark = 'o'
            if 'tree' in temp_label:
                temp_color = 'green'
            else:
                temp_color = 'magenta'
    # Summer days
    if poi.DOY.to_numpy()[0] > 90:
        ax1.plot(temp_hour, temp_utci, label=labelDict_[temp_label], color=temp_color, linestyle=temp_line, marker = temp_mark)
    # Winter days
    else:
        ax2.plot(temp_hour, temp_utci, label=labelDict_[temp_label], color=temp_color, linestyle=temp_line, marker = temp_mark)

# ax1.legend(prop={'size': 8})
ax1.set_ylabel('UTCI ($^\circ$C)')
# ax1.set_xlabel('Hour')
ax1.set_ylim(10, 50)
ax1.set_xlim(6, 20)
ax1.set_title('Summer', c='red')
# ax1.grid(True)

ax1.spines['bottom'].set_color('red')
ax1.spines['top'].set_color('red')
ax1.xaxis.label.set_color('red')
ax1.tick_params(axis='x', colors='red')

ax1.spines['left'].set_color('red')
ax1.spines['right'].set_color('red')
ax1.yaxis.label.set_color('red')
ax1.tick_params(axis='y', colors='red')

ax1.legend()

# ax2.legend(prop={'size': 8}, loc='upper left')
# ax2.set_ylabel('UTCI [$^\circ$C]')
# ax2.set_xlabel('Hour')
ax2.set_ylim(10, 50)
ax2.set_yticklabels([])
ax2.set_xlim(6, 20)
ax2.set_title('Winter', c='blue')
# ax2.grid(True)

ax2.spines['bottom'].set_color('blue')
ax2.spines['top'].set_color('blue')
ax2.xaxis.label.set_color('blue')
ax2.tick_params(axis='x', colors='blue')

ax2.spines['left'].set_color('blue')
ax2.spines['right'].set_color('blue')
ax2.tick_params(axis='y', colors='blue')

# Shared xlabel
fig.supxlabel('Hour', x=0.515)

# # Add shared legend at position in loc
# handles, labels = ax1.get_legend_handles_labels()
# fig.legend(handles, labels, loc=(0.434, 0.78), facecolor='white', framealpha=1)

fig.tight_layout()
fig.savefig(save_path + 'UTCI.png', dpi=300)

print('end')
