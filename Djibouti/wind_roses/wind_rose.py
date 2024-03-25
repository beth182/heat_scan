import os
import pandas as pd
from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
import numpy as np

mpl.rcParams.update({'font.size': 15})

current_dir = os.getcwd().replace('\\', '/') + '/'

file_path = current_dir + 'ERA5LAND_meteo.csv'

# read in file
df = pd.read_csv(file_path)

df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M')

# subset the pandas df for ony DJF and JJA
DJF_df = pd.concat(
    [df.loc[df.datetime.dt.month == 12], df.loc[df.datetime.dt.month == 1], df.loc[df.datetime.dt.month == 2]])

JJA_df = pd.concat(
    [df.loc[df.datetime.dt.month == 6], df.loc[df.datetime.dt.month == 7], df.loc[df.datetime.dt.month == 8]])

print('end')

# plotting
"""
# Summer
ax = WindroseAxes.from_ax(figsize=(10, 10))
ax.bar(JJA_df.WD, JJA_df.WS, normed=True, opening=0.8, edgecolor='white', cmap=cm.inferno, bins=np.arange(0, 12, 2))
ax.set_legend(loc='upper left', bbox_to_anchor=(0.58, 0.5))
plt.title('Summer')
plt.savefig(current_dir + 'summer_wind.png', bbox_inches='tight', dpi=300)
"""

"""
# Winter
ax = WindroseAxes.from_ax(figsize=(10, 10))
ax.bar(DJF_df.WD, DJF_df.WS, normed=True, opening=0.8, edgecolor='white', cmap=cm.inferno, bins=np.arange(0, 12, 2))
ax.set_legend(loc='upper left', bbox_to_anchor=(0.18, 0.5))
plt.title('Winter')
plt.savefig(current_dir + 'winter_wind.png', bbox_inches='tight', dpi=300)
"""

# NOTE: edits were made to the source code of the windrose package. In the file windorse.py, 2 functions were changed
# to better format the legend:

"""
    def set_legend(self, **pyplot_arguments):
        # Original code in comments

        legend = self.legend(borderaxespad=-0.10, **pyplot_arguments)
        plt.setp(legend.get_texts(), fontsize=15)
        return legend

        # if "borderaxespad" not in pyplot_arguments:
        #     pyplot_arguments["borderaxespad"] = -0.10
        # legend = self.legend(**pyplot_arguments)
        # plt.setp(legend.get_texts(), fontsize=8)
        # return legend
        
        
    def get_labels(decimal_places=1, units=None):
        # Original code in comments

        labels = np.copy(self._info['bins'])
        labels = ["%.1f : %0.1f" % (labels[i], labels[i + 1] - 0.1) \
                    for i in range(len(labels) - 1)]
        return labels

        # digits = np.copy(self._info["bins"]).tolist()
        # if not digits:
        #     return ""
        # digits[-1] = digits[-2]
        # digits = [f"{label:.{decimal_places}f}" for label in digits]
        # fmt = "[{} : {}"
        # if locale.getlocale()[0] in ["fr_FR"]:
        #     fmt += "["
        # else:
        #     fmt += ")"
        #
        # if units:
        #     fmt += " " + units
        #
        # labels = [
        #     fmt.format(digits[k], digits[k + 1]) for k in range(len(digits) - 1)
        # ]
        # labels[-1] = f">{digits[-1]}"
        # return labels
"""

print('end')
