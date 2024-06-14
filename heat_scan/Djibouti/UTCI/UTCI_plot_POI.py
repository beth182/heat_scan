import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import glob
import os
from matplotlib.lines import Line2D

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
# labelDict_ = {'Balbala_open_average_djf': 'Open present climate',
#               'Balbala_open_average_jja': 'Open present climate',
#               'Balbala_open_hot_djf': 'Open future climate',
#               'Balbala_open_hot_jja': 'Open future climate',
#               'Balbala_tree_average_djf': 'Tree present climate',
#               'Balbala_tree_average_jja': 'Tree present climate',
#               'Balbala_tree_hot_djf': 'Tree future climate',
#               'Balbala_tree_hot_jja': 'Tree future climate'}

labelDict_ = {'Balbala_open_average_djf': 'Open: Historical',
              'Balbala_open_average_jja': 'Open: Historical',
              'Balbala_open_hot_djf': 'Open: Future',
              'Balbala_open_hot_jja': 'Open: Future',
              'Balbala_tree_average_djf': 'Tree: Historical',
              'Balbala_tree_average_jja': 'Tree: Historical',
              'Balbala_tree_hot_djf': 'Tree: Future',
              'Balbala_tree_hot_jja': 'Tree: Future'}

# ax = plt.subplot(1, 1, 1, projection='polar')
fig = plt.figure(figsize=(12, 6), constrained_layout=True)
gs = fig.add_gridspec(1, 2)

# Add axes, i.e. subplots
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])

# assign empty dict for stats
array_dict = {}

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

        # OPEN HISTORICAL
        if 'open' in temp_label and 'average' in temp_label:
            ax1.plot(temp_hour, temp_utci, label=labelDict_[temp_label], color=temp_color, linestyle=temp_line,
                     marker=temp_mark, alpha=1)

        # OPEN FUTURE
        if 'open' in temp_label and 'hot' in temp_label:
            ax1.plot(temp_hour, temp_utci, label=labelDict_[temp_label], color=temp_color, linestyle=temp_line,
                     marker=temp_mark, alpha=1)

        # TREE HISTORICAL
        if 'tree' in temp_label and 'average' in temp_label:
            ax1.plot(temp_hour, temp_utci, label=labelDict_[temp_label], color=temp_color, linestyle=temp_line,
                     marker=temp_mark, alpha=1)

        # TREE FUTURE
        if 'tree' in temp_label and 'hot' in temp_label:
            ax1.plot(temp_hour, temp_utci, label=labelDict_[temp_label], color=temp_color, linestyle=temp_line,
                     marker=temp_mark, alpha=1)


        array_dict[temp_label] = temp_utci


    # Winter days
    else:

        # OPEN HISTORICAL
        if 'open' in temp_label and 'average' in temp_label:
            ax2.plot(temp_hour, temp_utci, label=labelDict_[temp_label], color=temp_color, linestyle=temp_line,
                     marker=temp_mark, alpha=1)

        # OPEN FUTURE
        if 'open' in temp_label and 'hot' in temp_label:
            ax2.plot(temp_hour, temp_utci, label=labelDict_[temp_label], color=temp_color, linestyle=temp_line,
                     marker=temp_mark, alpha=1)

        # TREE HISTORICAL
        if 'tree' in temp_label and 'average' in temp_label:
            ax2.plot(temp_hour, temp_utci, label=labelDict_[temp_label], color=temp_color, linestyle=temp_line,
                     marker=temp_mark, alpha=1)

        # TREE FUTURE
        if 'tree' in temp_label and 'hot' in temp_label:
            ax2.plot(temp_hour, temp_utci, label=labelDict_[temp_label], color=temp_color, linestyle=temp_line,
                     marker=temp_mark, alpha=1)


        array_dict[temp_label] = temp_utci


df = pd.DataFrame.from_dict(array_dict)

def percentage_change(col1,col2):
    return col2.sub(col1).div(col1).mul(100)

print('mean per diff between tree and open, summer, historical: ', percentage_change(df['Balbala_tree_average_jja'], df['Balbala_open_average_jja']).mean())
print('mean per diff between tree and open, summer, future: ', percentage_change(df['Balbala_tree_hot_jja'], df['Balbala_open_hot_jja']).mean())

print('mean per diff between tree and open, winter, historical: ', percentage_change(df['Balbala_tree_average_djf'], df['Balbala_open_average_djf']).mean())
print('mean per diff between tree and open, winter, future: ', percentage_change(df['Balbala_tree_hot_djf'], df['Balbala_open_hot_djf']).mean())

ax1.set_ylabel('Universal Thermal Climate Index ($^\circ$C)')
ax1.set_ylim(10, 50)
ax1.set_xlim(6, 20)
ax1.set_title('Summer', c='red')
ax1.grid(True)

# call legend according to pre-defined labels
# leg = ax1.legend()
# for lh in leg.legendHandles:
#     lh.set_alpha(1)

# manually create legend
# line_historical = Line2D([0], [0], color='k', linestyle='-')
# line_future = Line2D([0], [0], color='k', linestyle=':')
# ax1.legend(handles=[line_historical, line_future], labels= ['Historical', 'Future'])

ax2.set_ylim(10, 50)
ax2.set_yticklabels([])
ax2.set_xlim(6, 20)
ax2.set_title('Winter', c='blue')
ax2.grid(True)

ax1.axhspan(9, 26, alpha=0.2, color='green')
ax2.axhspan(9, 26, alpha=0.2, color='green')

ax1.axhspan(26, 32, alpha=0.8, color='lightgoldenrodyellow')
ax2.axhspan(26, 32, alpha=0.8, color='lightgoldenrodyellow')

ax1.axhspan(32, 38, alpha=0.3, color='goldenrod')
ax2.axhspan(32, 38, alpha=0.3, color='goldenrod')

ax1.axhspan(38, 46, alpha=0.3, color='indianred')
ax2.axhspan(38, 46, alpha=0.3, color='indianred')

ax1.axhspan(46, 100, alpha=0.3, color='darkred')
ax2.axhspan(46, 100, alpha=0.3, color='darkred')

# Shared xlabel
fig.supxlabel('Hour', x=0.515, y=0.05)

fig.tight_layout()
# fig.savefig(save_path + 'UTCI_V4.png', dpi=300)

fig.savefig(save_path + 'UTCI.png', dpi=300)

print('end')
