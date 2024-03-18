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

background = 'light'

tz = 'Africa/Djibouti'
lat, lon = 11.588016341753459, 43.14789764878434

times = pd.date_range('1993-07-21 00:00:00', '2015-08-13', inclusive='left',
                      freq='H', tz=tz)
solpos = solarposition.get_solarposition(times, lat, lon)
# remove nighttime
solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]

if background == 'dark':
    plt.style.use('dark_background')

fig = plt.figure(figsize=(12, 6))
# ax = plt.subplot(1, 1, 1, projection='polar')
ax = fig.add_subplot(1, 1, 1, projection='polar')

datesOfInterest = ['2000-02-21', '2007-01-21', '1993-07-21', '2015-08-13']
dateLabels = ['Average winter climate (future)', 'Average winter climate (present)', 'Average summer climate (present)',
              'Average summer climate (future)']
datecolors = ['blue', 'blue', 'red', 'red']
datelinetype = [':', '-', '-', ':']

# draw individual days
for date in pd.to_datetime(datesOfInterest):
    times = pd.date_range(date, date + pd.Timedelta('24h'), freq='5min', tz=tz)
    solpos = solarposition.get_solarposition(times, lat, lon)
    solpos = solpos.loc[solpos['apparent_elevation'] > 0, :]
    label = dateLabels[np.where(pd.to_datetime(datesOfInterest) == date)[0][0]]
    col = datecolors[np.where(pd.to_datetime(datesOfInterest) == date)[0][0]]
    linet = datelinetype[np.where(pd.to_datetime(datesOfInterest) == date)[0][0]]
    ax.plot(np.radians(solpos.azimuth).values, solpos.apparent_zenith.values, label=label, c=col, linestyle=linet,
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

ax.set_xticklabels(['N', '', 'E', '', 'S', '', 'W', ''], color='k')

# Add shared legend at position in loc
handles, labels = ax.get_legend_handles_labels()
# ax.figure.legend(handles, labels, ncol=2, fontsize=9, loc='lower left')

fig.tight_layout()
fig.savefig(save_path + background + '_solarpath.png', dpi=300, transparent=True)

# plt.show()
print('end')