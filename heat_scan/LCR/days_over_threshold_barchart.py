import os
import pandas as pd
import numpy as np
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

# where there are less days in 2050 than 2015:
# return to original
df_median_days['2050_new'] = df_median_days['2050']
df_median_days['2050_new'][np.where(df_median_days['2050'] < 0)[0]] = df_median_days['2050'][np.where(df_median_days['2050'] < 0)[0]] + df_median_days['2015'][np.where(df_median_days['2050'] < 0)[0]]

# change the 2015 one: 2015 take the smaller 2050
df_median_days['2015_new'] = df_median_days['2015']
df_median_days['2015_new'][np.where(df_median_days['2050'] < 0)[0]] = df_median_days['2015'][np.where(df_median_days['2050'] < 0)[0]] - df_median_days['2050_new'][np.where(df_median_days['2050'] < 0)[0]]


# 2100
df_median_days['2100'] = df_median_days['2100 Median days'] - df_median_days['2015_new'] - df_median_days['2050_new']

# where there are less days in 2100 than 2050

# make sure that, if 2100 is smaller than 2015, it is also smaller than 2050
assert np.where(df_median_days['2100 Median days'] < df_median_days['2050 Median days'])[0].all() == np.where(df_median_days['2100 Median days'] < df_median_days['2015 Median days'])[0].all()
assert np.where(df_median_days['2100 Median days'] < df_median_days['2050 Median days'])[0].any() == np.where(df_median_days['2100 Median days'] < df_median_days['2015 Median days'])[0].any()

# return to original
df_median_days['2100_new'] = df_median_days['2100']
df_median_days['2100_new'][np.where(df_median_days['2100'] < 0)[0]] = df_median_days['2100'][np.where(df_median_days['2100'] < 0)[0]] + df_median_days['2015_new'][np.where(df_median_days['2100'] < 0)[0]] + df_median_days['2050_new'][np.where(df_median_days['2100'] < 0)[0]]

# change the 2050 one: 2050 take the smaller 2100
df_median_days['2050_new_2'] = df_median_days['2100_new']
df_median_days['2050_new_2'][np.where(df_median_days['2100'] < 0)[0]] = df_median_days['2050_new'][np.where(df_median_days['2100'] < 0)[0]] - df_median_days['2100_new'][np.where(df_median_days['2100'] < 0)[0]]

print('end')



df_median_days[['2015_new', '2050_new_2', '2100_new']].plot.bar(stacked=True)











fig, ax = plt.subplots()

colors = pd.Series({
    '2015_new':'C0',
    '2100_new':'C1',
    '2050_new_2':'C2'
})

test = df_median_days[['2015_new', '2100_new', '2050_new_2']]

for i,r in test.iterrows():
    row = r.sort_values().cumsum()[::-1]
    ax.bar([i]*len(row), row, color=row.index.map(colors))


plt.xticks(rotation=90)




print('end')

df_median_days['2050'][np.where(df_median_days['2050'] < 0)[0]] = -(df_median_days['2050'][np.where(df_median_days['2050'] < 0)[0]] + df_median_days['2015'][np.where(df_median_days['2050'] < 0)[0]])
df_median_days['2100'][np.where(df_median_days['2100'] < 0)[0]] = -(df_median_days['2100'][np.where(df_median_days['2100'] < 0)[0]] + df_median_days['2050 Median days'][np.where(df_median_days['2100'] < 0)[0]])

# make sure where 2100 is negative, 2050 is also negative
assert len(np.where(df_median_days['2050'][np.where(df_median_days['2100'] < 0)[0]] > 0)[0]) == 0

# make sure 2100 is always more negative than 2050
assert len(np.where(df_median_days['2050'][np.where(df_median_days['2100'] < 0)[0]] > df_median_days['2100'][np.where(df_median_days['2100'] < 0)[0]])[0]) == 0


df_median_days['2100'][np.where(df_median_days['2100'] < 0)[0]] = -np.abs(df_median_days['2100'][np.where(df_median_days['2100'] < 0)[0]] - df_median_days['2050'][np.where(df_median_days['2100'] < 0)[0]])


df_median_days[['2015', '2050', '2100']].plot.bar(stacked=True)


print('end')
