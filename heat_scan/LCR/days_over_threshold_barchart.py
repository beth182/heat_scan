import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

import matplotlib

matplotlib.use('TkAgg')
matplotlib.rcParams.update({'font.size': 15})


def read_csvs_for_bar(years, current_dir=os.getcwd().replace('\\', '/') + '/', test=False, scale='Country'):
    """

    :return:
    """
    # ToDo: docstring here

    if test:
        test_flag = '_test'
    else:
        test_flag = ''

    df_list = []
    for year in years:
        # read in csv files

        if scale == 'Country':
            csv_name = current_dir + str(year) + '_days_over_' + str(threshold) + '_' + source_id + test_flag + '.csv'
        else:
            assert scale == 'City'
            csv_name = current_dir + 'cities_' + year + '_GFDL-ESM4_ssp245.csv'

        assert os.path.isfile(csv_name)

        df = pd.read_csv(csv_name)
        if 'Unnamed: 0' in df.columns:
            df = df.drop(columns=['Unnamed: 0'])
        df = df.add_prefix(str(year) + ' ')

        df = df.fillna(0)

        df = df.rename(columns={str(year) + ' ' + scale: scale, str(year) + ' Median days': str(year)})

        if scale == 'City':
            df['City'] = df['City'] + ', ' + df[str(year) + ' Country']

        df = df[[scale, str(year)]]

        df.index = df[scale]
        df = df.drop(columns=[scale])

        df_list.append(df)

    df_median_days = pd.concat(df_list, axis=1)

    return df_median_days


def grouped_bar(years, threshold, ssp, source_id, current_dir=os.getcwd().replace('\\', '/') + '/', test=False,
                scale='Country'):
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

    df_median_days = read_csvs_for_bar(years=years, current_dir=current_dir, test=test, scale=scale)

    # sort by 2100
    df_median_days = df_median_days.sort_values(by='2090_to_2100', ascending=False)

    color_df = {'2090_to_2100': 'orange', '2040_to_2050': 'purple', '2015_to_2025': 'black'}

    fig, ax = plt.subplots(1, figsize=(17, 12))

    df_median_days.plot.bar(ax=ax, color=color_df)

    if scale == 'Country':
        font_size = 10
    else:
        assert scale == 'City'
        font_size = 5

    ax.tick_params(axis='x', labelsize=font_size)
    plt.xticks(rotation=45, ha="right")

    plt.ylabel('Number of days over threshold')
    plt.xlabel(scale)

    plt.title(
        'Number of days where daily maximum near-surface air temperature > ' + str(
            threshold) + '$^{\circ}$C for ' + ssp + ': ' + scale + '-scale')

    ax.legend(["2015 to 2025", "2040 to 2050", "2090 to 2100"])

    plt.savefig(
        current_dir + scale + '_days_over_' + str(
            threshold) + '_' + ssp + '_' + source_id + test_flag + '_grouped.png',
        bbox_inches='tight', dpi=300)

    print('end')


def stacked_bar(years, threshold, ssp, source_id, current_dir=os.getcwd().replace('\\', '/') + '/',
                test=False, scale='Country'):
    """

    :param threshold:
    :param ssp:
    :param source_id:
    :param current_dir:
    :param test:
    :return:
    """
    # ToDo: docstring here

    # needs to be these years otherwise this function doesnt work
    # ToDo: fix this issue
    assert years == ['2015_to_2025', '2040_to_2050', '2090_to_2100']

    if test:
        test_flag = '_test'
    else:
        test_flag = ''

    df_median_days = read_csvs_for_bar(years=years, current_dir=current_dir, test=test, scale=scale)

    # sort by 2100
    df_median_days = df_median_days.sort_values(by='2090_to_2100', ascending=False)

    df_median_days['low'] = 0
    df_median_days['mid'] = 0
    df_median_days['high'] = 0

    df_median_days['low_year'] = 0
    df_median_days['mid_year'] = 0
    df_median_days['high_year'] = 0

    for index, row in df_median_days.iterrows():

        for year in years:

            if row[str(year)] == row[[str(i) for i in years]].min():
                row['low'] = row[str(year)]
                row['low_year'] = str(year)

            elif row[str(year)] == row[[str(i) for i in years]].max():
                row['high'] = row[str(year)]
                row['high_year'] = str(year)

            else:
                row['mid'] = row[str(year)]
                row['mid_year'] = str(year)

            df_median_days.loc[index] = row

    # get rid of zeros
    zero_ind = np.where(df_median_days.mid_year == 0)[0]

    # assert df_median_days['2040_to_2050'][zero_ind].sum() == 0
    # assert df_median_days['2015_to_2025'][zero_ind].sum() == 0
    df_median_days['mid_year'][zero_ind] = '2015_to_2025'

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

    color_df = {'2015_to_2025': 'black', '2040_to_2050': 'purple', '2090_to_2100': 'orange'}
    fig, ax = plt.subplots(1, figsize=(17, 12))

    # plot in correct order
    high_df['2090_to_2100'].plot.bar(ax=ax, color=color_df['2090_to_2100'], width=0.80)
    high_df['2040_to_2050'].plot.bar(ax=ax, color=color_df['2040_to_2050'], width=0.80)
    high_df['2015_to_2025'].plot.bar(ax=ax, color=color_df['2015_to_2025'], width=0.80)

    mid_df['2090_to_2100'].plot.bar(ax=ax, color=color_df['2090_to_2100'], label='', width=0.80)
    mid_df['2040_to_2050'].plot.bar(ax=ax, color=color_df['2040_to_2050'], label='', width=0.80)
    mid_df['2015_to_2025'].plot.bar(ax=ax, color=color_df['2015_to_2025'], label='', width=0.80)

    low_df['2090_to_2100'].plot.bar(ax=ax, color=color_df['2090_to_2100'], label='', width=0.80)
    low_df['2040_to_2050'].plot.bar(ax=ax, color=color_df['2040_to_2050'], label='', width=0.80)
    low_df['2015_to_2025'].plot.bar(ax=ax, color=color_df['2015_to_2025'], label='', width=0.80)

    plt.legend(["2015 to 2025", "2040 to 2050", "2090 to 2100"])

    if scale == 'Country':
        font_size = 10
    else:
        assert scale == 'City'
        font_size = 4

    ax.tick_params(axis='x', labelsize=font_size)
    plt.xticks(rotation=45, ha="right")

    plt.ylabel('Number of days over threshold')
    plt.xlabel(scale)

    plt.title(
        'Number of days where daily maximum near-surface air temperature > ' + str(
            threshold) + '$^{\circ}$C for ' + ssp + ': ' + scale + '-scale')

    plt.savefig(
        current_dir + scale + '_days_over_' + str(
            threshold) + '_' + ssp + '_' + source_id + test_flag + '_stacked.png',
        bbox_inches='tight', dpi=300)

    print('end')


if __name__ == "__main__":
    threshold = 30
    ssp = 'SSP245'

    source_id = 'GFDL-ESM4'
    # source_id = 'ACCESS-CM2'

    years = ['2015_to_2025', '2040_to_2050', '2090_to_2100']

    # stacked_bar(years=years, threshold=threshold, ssp=ssp, source_id=source_id, scale='Country')
    stacked_bar(years=years, threshold=threshold, ssp=ssp, source_id=source_id, scale='City')

    # grouped_bar(years=years, threshold=threshold, ssp=ssp, source_id=source_id, scale='Country')
    # grouped_bar(years=years, threshold=threshold, ssp=ssp, source_id=source_id, scale='City')

    print('end')
