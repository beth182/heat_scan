# imports
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

import matplotlib

matplotlib.use('TkAgg')
matplotlib.rcParams.update({'font.size': 15})

# COUNTY

# read in the csvs

current_dir = os.getcwd().replace('\\', '/') + '/'

path_2015 = current_dir + 'cities_2015_to_2025_GFDL-ESM4_ssp245.csv'
path_2050 = current_dir + 'cities_2040_to_2050_GFDL-ESM4_ssp245.csv'
path_2100 = current_dir + 'cities_2090_to_2100_GFDL-ESM4_ssp245.csv'

assert os.path.isfile(path_2100)
assert os.path.isfile(path_2050)
assert os.path.isfile(path_2015)

df_2100 = pd.read_csv(path_2100)
df_2050 = pd.read_csv(path_2050)
df_2015 = pd.read_csv(path_2015)

df_2100 = df_2100[['City', 'Median days']]
df_2100.index = df_2100.City
df_2100 = df_2100.drop(columns=['City'])
df_2100 = df_2100.rename(columns={'Median days': '2100'})

df_2050 = df_2050[['City', 'Median days']]
df_2050.index = df_2050.City
df_2050 = df_2050.drop(columns=['City'])
df_2050 = df_2050.rename(columns={'Median days': '2050'})

df_2015 = df_2015[['City', 'Median days']]
df_2015.index = df_2015.City
df_2015 = df_2015.drop(columns=['City'])
df_2015 = df_2015.rename(columns={'Median days': '2015'})

df = pd.concat([df_2015, df_2050, df_2100], axis=1)

# read in cities csv
path_cities = current_dir + 'UN_2015_cities_over_300k.csv'
assert os.path.isfile(path_cities)
df_cities = pd.read_csv(path_cities)

df_cities.index = df_cities.City


df = pd.concat([df, df_cities[['latitude', 'Country']]], axis=1)

df = df.dropna()

df['end_century_diff'] = df['2100'] - df['2015']


fig, ax = plt.subplots(1, figsize=(10,10))

df_bar = df.groupby('Country').mean()[['end_century_diff']].sort_values('end_century_diff', ascending=False)
df_bar.plot.bar(ax=ax, color='purple', width=0.8, label='')
ax.tick_params(axis='x', labelsize=10)
plt.xticks(rotation=45, ha="right")
ax.axhline(y=0, color='orange', linestyle=':')

ax.set_xlabel('Country')
ax.set_ylabel('Additional hot days (30$^\circ$ or higher)')

plt.title('Average increase in the number of hot days (from 2015-2015 to 2090-2100)' + "\n" + ' for cities of a given country')
ax.get_legend().remove()

plt.savefig(current_dir + 'cities_countries_increase.png', bbox_inches='tight', dpi=300)
print('end')



# scatter plot of days differance vs. distance from the equator
"""
x = np.asarray(np.abs(df.latitude))
y = np.asarray(df['2100'] - df['2015'])

plt.figure(figsize=(10, 10))

plt.axhline(y=0, color='orange', linestyle=':')

plt.scatter(x, y, marker='x', c='purple')

gradient, intercept, r_value, p_value, std_err = stats.linregress(x, y)

mn = np.min(x)
mx = np.max(x)
x1 = np.linspace(mn, mx, 500)
y1 = gradient * x1 + intercept
plt.plot(x1, y1, '--k')

plt.xlim(mn, mx)
plt.ylim(min(y) - 5, max(y) + 5)

plt.xlabel('Distance from the equator ($^\circ$)')
plt.ylabel('Additional hot days (30$^\circ$ or higher)')

plt.title(
    'LCR Cities: Increase in hot days (from 2015-2015 to 2090-2100)' + "\n" + ' and their distance from the equator')

plt.savefig(current_dir + 'cities_equator_distance.png', bbox_inches='tight', dpi=300)
"""

print('end')
