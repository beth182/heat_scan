import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

import matplotlib

matplotlib.use('TkAgg')
matplotlib.rcParams.update({'font.size': 15})


def read_csvs_for_bar(current_dir=os.getcwd().replace('\\', '/') + '/', test=False):
    """

    :return:
    """
    # ToDo: docstring here
    years = [2015, 2050, 2100]

    if test:
        test_flag = '_test'
    else:
        test_flag = ''

    df_list = []
    for year in years:
        # read in csv files
        csv_name = current_dir + str(year) + '_days_over_' + str(threshold) + '_' + source_id + test_flag + '.csv'
        assert os.path.isfile(csv_name)

        df = pd.read_csv(csv_name)
        df = df.drop(columns=['Unnamed: 0'])
        df = df.add_prefix(str(year) + ' ')

        df = df.fillna(0)

        df_list.append(df)

    df = pd.concat(df_list, axis=1)

    df_median_days = df[['2015 Country', '2015 Median days', '2050 Median days', '2100 Median days']]
    df_median_days = df_median_days.rename(
        columns={'2015 Country': 'Country', '2015 Median days': '2015', '2050 Median days': '2050',
                 '2100 Median days': '2100'})
    df_median_days.index = df_median_days.Country
    df_median_days = df_median_days.drop(columns=['Country'])

    return df_median_days


def grouped_bar(threshold, ssp, source_id, current_dir=os.getcwd().replace('\\', '/') + '/', test=False):
    """

    :param threshold:
    :param ssp:
    :param source_id:
    :param current_dir:
    :param test:
    :return:
    """
    # ToDo: docstring here

    if test:
        test_flag = '_test'
    else:
        test_flag = ''

    df_median_days = read_csvs_for_bar(current_dir=current_dir, test=test)

    # sort by 2100
    df_median_days = df_median_days.sort_values(by='2100', ascending=False)

    color_df = {'2015': 'black', '2050': 'purple', '2100': 'orange'}
    fig, ax = plt.subplots(1, figsize=(17, 12))

    df_median_days.plot.bar(ax=ax, color=color_df)

    ax.tick_params(axis='x', labelsize=10)
    plt.xticks(rotation=45, ha="right")

    plt.ylabel('Median number of days over threshold')
    plt.xlabel('Country')

    plt.title(
        'Number of days where daily maximum near-surface air temperature > ' + str(
            threshold) + '$^{\circ}$C for ' + ssp)

    plt.savefig(
        current_dir + 'countries_days_over_' + str(
            threshold) + '_' + ssp + '_' + source_id + test_flag + '_grouped.png',
        bbox_inches='tight', dpi=300)
    print('end')


def stacked_bar(threshold, ssp, source_id, current_dir=os.getcwd().replace('\\', '/') + '/', test=False):
    """

    :param threshold:
    :param ssp:
    :param source_id:
    :param current_dir:
    :param test:
    :return:
    """
    # ToDo: docstring here

    years = [2015, 2050, 2100]

    if test:
        test_flag = '_test'
    else:
        test_flag = ''

    df_median_days = read_csvs_for_bar(current_dir=current_dir, test=test)

    # sort by 2015
    df_median_days = df_median_days.sort_values(by='2015', ascending=False)

    df_median_days['low'] = 0
    df_median_days['mid'] = 0
    df_median_days['high'] = 0

    df_median_days['low_year'] = 0
    df_median_days['mid_year'] = 0
    df_median_days['high_year'] = 0

    for index, row in df_median_days.iterrows():

        for year in years:

            if row[str(year)] == row[['2015', '2050', '2100']].min():
                row['low'] = row[str(year)]
                row['low_year'] = str(year)

            elif row[str(year)] == row[['2015', '2050', '2100']].max():
                row['high'] = row[str(year)]
                row['high_year'] = str(year)

            else:
                row['mid'] = row[str(year)]
                row['mid_year'] = str(year)

        df_median_days.loc[index] = row

    # get rif of zeros
    zero_ind = np.where(df_median_days.mid_year == 0)[0]
    assert df_median_days['2050'][zero_ind].sum() == 0
    assert df_median_days['2015'][zero_ind].sum() == 0
    df_median_days['mid_year'][zero_ind] = '2015'

    low_df = df_median_days[['low', 'low_year']]
    low_df = low_df.pivot_table(values='low', index=low_df.index, columns='low_year', aggfunc='first')

    high_df = df_median_days[['high', 'high_year']]
    high_df = high_df.pivot_table(values='high', index=high_df.index, columns='high_year', aggfunc='first')

    mid_df = df_median_days[['mid', 'mid_year']]
    mid_df = mid_df.pivot_table(values='mid', index=mid_df.index, columns='mid_year', aggfunc='first')

    # make sure all three have all years as colums
    for year in years:

        for df_here in [low_df, mid_df, high_df]:

            if str(year) in df_here.columns:
                pass
            else:
                df_here[str(year)] = 0

    # replace all nan's
    low_df = low_df.fillna(0)
    high_df = high_df.fillna(0)
    mid_df = mid_df.fillna(0)

    low_df = low_df.reindex(df_median_days.index)
    high_df = high_df.reindex(df_median_days.index)
    mid_df = mid_df.reindex(df_median_days.index)

    color_df = {'2015': 'black', '2050': 'purple', '2100': 'orange'}
    fig, ax = plt.subplots(1, figsize=(17, 12))

    # plot in correct order
    high_df['2100'].plot.bar(ax=ax, color=color_df['2100'])
    high_df['2050'].plot.bar(ax=ax, color=color_df['2050'])
    high_df['2015'].plot.bar(ax=ax, color=color_df['2015'])

    mid_df['2100'].plot.bar(ax=ax, color=color_df['2100'], label='')
    mid_df['2050'].plot.bar(ax=ax, color=color_df['2050'], label='')
    mid_df['2015'].plot.bar(ax=ax, color=color_df['2015'], label='')

    low_df['2100'].plot.bar(ax=ax, color=color_df['2100'], label='')
    low_df['2050'].plot.bar(ax=ax, color=color_df['2050'], label='')
    low_df['2015'].plot.bar(ax=ax, color=color_df['2015'], label='')

    plt.legend()
    ax.tick_params(axis='x', labelsize=10)
    plt.xticks(rotation=45, ha="right")

    plt.ylabel('Median number of days over threshold')
    plt.xlabel('Country')

    plt.title(
        'Number of days where daily maximum near-surface air temperature > ' + str(
            threshold) + '$^{\circ}$C for ' + ssp)

    plt.savefig(
        current_dir + 'countries_days_over_' + str(
            threshold) + '_' + ssp + '_' + source_id + test_flag + '_stacked.png',
        bbox_inches='tight', dpi=300)
    print('end')


if __name__ == "__main__":
    threshold = 30
    ssp = 'SSP245'

    source_id = 'GFDL-ESM4'
    # source_id = 'ACCESS-CM2'

    # stacked_bar(threshold=threshold, ssp=ssp, source_id=source_id)
    grouped_bar(threshold=threshold, ssp=ssp, source_id=source_id)

    print('end')
