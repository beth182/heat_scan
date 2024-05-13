import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')
matplotlib.rcParams.update({'font.size': 15})

# ToDo: put into functions!

# read in csv files
current_dir = os.getcwd().replace('\\', '/') + '/'

years = [2015, 2050, 2100]
threshold = 30
ssp = 'SSP245'

df_list = []
for year in years:
    csv_name = current_dir + str(year) + '_days_over_' + str(threshold) + '.csv'
    assert os.path.isfile(csv_name)

    df = pd.read_csv(csv_name)
    df = df.drop(columns=['Unnamed: 0'])
    df = df.add_prefix(str(year) + ' ')

    df = df.fillna(0)

    df_list.append(df)

df = pd.concat(df_list, axis=1)

df_median_days = df[['2015 Country', '2015 Median days', '2050 Median days', '2100 Median days']]
df_median_days = df_median_days.rename(columns={'2015 Country': 'Country', '2015 Median days': '2015', '2050 Median days': '2050', '2100 Median days': '2100'})
df_median_days.index = df_median_days.Country
df_median_days = df_median_days.drop(columns=['Country'])

# sort by 2015
df_median_days = df_median_days.sort_values(by='2015', ascending=False)


color_df = {'2015': 'black', '2050': 'purple', '2100': 'orange'}
fig, ax = plt.subplots(1, figsize=(17, 12))

df_median_days['2100'].plot.bar(ax=ax, color=color_df['2100'])
df_median_days['2050'].plot.bar(ax=ax, color=color_df['2050'])
df_median_days['2015'].plot.bar(ax=ax, color=color_df['2015'])

small_2050_ind = np.where(df_median_days['2050'] < df_median_days['2015'])[0]

small_2100_ind = np.where(df_median_days['2100'] < df_median_days['2015'])[0]

# plot over the top of the existing where bars are covered up
# init a zeros df
zeros_df = pd.DataFrame(0, index=df_median_days.index, columns=df_median_days.columns)

# fill zeros df with these smaller vals
zeros_df['2050'][small_2050_ind] = df_median_days['2050'][small_2050_ind]
zeros_df['2100'][small_2100_ind] = df_median_days['2100'][small_2100_ind]

assert (zeros_df['2100'] <= zeros_df['2050']).all()
assert (zeros_df['2100'] <= zeros_df['2050']).any()

# plot over the top
zeros_df['2050'].plot.bar(ax=ax, color=color_df['2050'], label='')
zeros_df['2100'].plot.bar(ax=ax, color=color_df['2100'], label='')

plt.legend()
ax.tick_params(axis='x', labelsize=10)
plt.xticks(rotation=45, ha="right")

plt.ylabel('Median number of days over threshold')
plt.xlabel('Country')

plt.title('Number of days where daily maximum near-surface air temperature > ' + str(threshold) + '$^{\circ}$C for ' + ssp)

plt.savefig(current_dir + 'countries_days_over_' + str(threshold) + '_' + ssp + '.png', bbox_inches='tight', dpi=300)
print('end')

# plt.scatter(df['2015 Country'], (df['2015 Median temp'] - df['2015 Mean temp'])/df['2015 Mean temp'])
# plt.xticks(rotation=90)