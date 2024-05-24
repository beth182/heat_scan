# imports
import os
import pandas as pd
import numpy as np

# COUNTY

# read in the csvs

current_dir = os.getcwd().replace('\\', '/') + '/'




path_2100 = current_dir + '2090_to_2100_days_over_30_GFDL-ESM4.csv'
path_2050 = current_dir + '2040_to_2050_days_over_30_GFDL-ESM4.csv'
path_2015 = current_dir + '2015_to_2025_days_over_30_GFDL-ESM4.csv'

assert os.path.isfile(path_2100)
assert os.path.isfile(path_2050)
assert os.path.isfile(path_2015)

df_2100 = pd.read_csv(path_2100)
df_2100 = df_2100[['Country', 'Median days']]
df_2100.index = df_2100.Country
df_2100 = df_2100.drop(columns=['Country'])
df_2100 = df_2100.rename(columns={'Median days': '2100'})

df_2050 = pd.read_csv(path_2050)
df_2050 = df_2050[['Country', 'Median days']]
df_2050.index = df_2050.Country
df_2050 = df_2050.drop(columns=['Country'])
df_2050 = df_2050.rename(columns={'Median days': '2050'})

df_2015 = pd.read_csv(path_2015)
df_2015 = df_2015[['Country', 'Median days']]
df_2015.index = df_2015.Country
df_2015 = df_2015.drop(columns=['Country'])
df_2015 = df_2015.rename(columns={'Median days': '2015'})


df = pd.concat([df_2015, df_2050, df_2100], axis=1)

# regions
region_path = current_dir + 'countries_in_LCR.csv'
assert os.path.isfile(region_path)

region_df = pd.read_csv(region_path)

region_df.index = region_df.Country
region_df = region_df.drop(columns=['Country'])

df = pd.concat([df, region_df], axis=1)

# countries where there is not an increase in number of days:
# df.iloc[np.where(df['2015'] > df['2100'])[0]]


# mean number of days increase from current to end centuary: for countries where there is an increase
# increase_countries = df.iloc[np.where(df['2015'] <= df['2100'])[0]]
# np.mean(increase_countries['2100'] - increase_countries['2015'])

# increase_countries = df.iloc[np.where(df['2015'] <= df['2050'])[0]]
# np.mean(increase_countries['2050'] - increase_countries['2015'])


# largest number of days by region
# df_SA = df.iloc[np.where(df['Subregion'] == 'South America')[0]]
# df_CA = df.iloc[np.where(df['Subregion'] == 'Central America')[0]]
# df_CI = df.iloc[np.where(df['Subregion'] == 'Caribbean')[0]]
#
# assert len(df_SA) + len(df_CA) + len(df_CI) == len(df)
#
# increase_countries_SA = df_SA.iloc[np.where(df_SA['2015'] <= df_SA['2100'])[0]]
# increase_countries_CA = df_CA.iloc[np.where(df_CA['2015'] <= df_CA['2100'])[0]]
# increase_countries_CI = df_CI.iloc[np.where(df_CI['2015'] <= df_CI['2100'])[0]]
#
# np.mean(increase_countries_SA['2100'] - increase_countries_SA['2015'])
# np.mean(increase_countries_CA['2100'] - increase_countries_CA['2015'])
# np.mean(increase_countries_CI['2100'] - increase_countries_CI['2015'])

# population
# pop_tot = df_CA['Population (2023)'].sum() + df_SA['Population (2023)'].sum() + df_CI['Population (2023)'].sum()
# df_CA['Population (2023)'].sum() / pop_tot



print('end')