import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

# read in csv files

current_dir = os.getcwd().replace('\\', '/') + '/'

years = [2015, 2050, 2100]
threshold = 30

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
df_median_days = df_median_days.rename(columns={'2015 Country': 'Country'})
df_median_days.index = df_median_days.Country
df_median_days = df_median_days.drop(columns=['Country'])

df_median_days['2015'] = df_median_days['2015 Median days']
df_median_days['2050'] = df_median_days['2050 Median days'] - df_median_days['2015 Median days']
df_median_days['2100'] = df_median_days['2100 Median days'] - df_median_days['2050 Median days']

df_median_days[['2015', '2050', '2100']].plot.bar(stacked=True)

# df_median_days.plot.bar(stacked=True)
print('end')
