from pvlib import solarposition
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

import matplotlib

matplotlib.use('TkAgg')

# original photo links: https://www.istockphoto.com/photo/fisheye-perspective-of-trees-in-forest-gm141468118-78244507
# https://www.istockphoto.com/photo/around-on-sky-taken-with-a-fisheye-lens-to-give-the-special-plate-effect-the-fresh-gm1250118657-364512394

save_path = os.getcwd().replace('\\', '/') + '/'

# background = 'light'
background = 'dark'

tz = 'Africa/Djibouti'
lat, lon = 11.588016341753459, 43.14789764878434

times = pd.date_range('1993-07-21 00:00:00', '2015-08-13', inclusive='left',
                      freq='H', tz=tz)
solpos = solarposition.get_solarposition(times, lat, lon)
# remove nighttime
solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

if background == 'dark':
    plt.style.use('dark_background')
    label_c = 'green'
else:
    label_c = 'magenta'

fig = plt.figure(figsize=(12, 6))
# ax = plt.subplot(1, 1, 1, projection='polar')
ax = fig.add_subplot(1, 1, 1, projection='polar')

# datesOfInterest = ['2000-02-21', '2007-01-21', '1993-07-21', '2015-08-13']
# dateLabels = ['Average winter climate (future)', 'Average winter climate (present)', 'Average summer climate (present)',
#               'Average summer climate (future)']
# datecolors = ['blue', 'blue', 'red', 'red']
# datelinetype = [':', '-', '-', ':']

datesOfInterest = ['2007-01-21', '1993-07-21']
dateLabels = ['Average winter climate (present)', 'Average summer climate (present)']
datecolors = ['blue', 'red']
datelinetype = ['-', '-']

# draw individual days
for date in pd.to_datetime(datesOfInterest):
    times = pd.date_range(date, date + pd.Timedelta('24h'), freq='5min', tz=tz)
    solpos = solarposition.get_solarposition(times, lat, lon)
    solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]
    label = dateLabels[np.where(pd.to_datetime(datesOfInterest) == date)[0][0]]
    col = datecolors[np.where(pd.to_datetime(datesOfInterest) == date)[0][0]]
    linet = datelinetype[np.where(pd.to_datetime(datesOfInterest) == date)[0][0]]
    ax.plot(np.radians(solpos.azimuth).values, solpos.apparent_zenith.values, c=col, linestyle=linet,
            linewidth=3)

    # just hours
    solpos_hour = solpos.iloc[np.where(solpos.index.minute == 0)[0]]
    ax.scatter(np.radians(solpos_hour.azimuth).values, solpos_hour.apparent_zenith.values, marker='o', s=120, c=col)

    for i in range(0, len(solpos_hour)):
        ax.text(np.radians(solpos_hour.azimuth).values[i], solpos_hour.apparent_zenith.values[i],
                solpos_hour.index.hour.astype(str)[i],
                horizontalalignment='center', verticalalignment='center', fontsize=8, color='white', style='oblique',
                weight="bold")

# change coordinates to be like a compass
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rmax(90)

ax.set_rlabel_position(0)
# ax.set_yticks([20,40,60,80])
plt.setp(ax.get_yticklabels()[::2], visible=False)

ax.set_xticklabels(['N', '', 'E', '', 'S', '', 'W', ''], color=label_c, fontsize=20)

import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

green_patch = mpatches.Patch(color='green', label='Trees')
magenta_patch = mpatches.Patch(color='magenta', label='Open')

red_patch = mpatches.Patch(color='red', label='Summer')
blue_patch = mpatches.Patch(color='blue', label='Winter')

present_line = Line2D([0], [0], label='Present Climate', color='k', linestyle='-')
future_line = Line2D([0], [0], label='Future Climate', color='k', linestyle=':')

# ax.figure.legend(handles=[green_patch, magenta_patch, red_patch, blue_patch, present_line, future_line], ncol=3,
#                  loc='lower left', fontsize=20, framealpha=1)

ax.spines['polar'].set_color(label_c)
ax.spines['polar'].set_linewidth(6)

fig.tight_layout()
fig.savefig(save_path + background + '_solarpath.png', dpi=300, transparent=True)

# plt.show()
print('end')
