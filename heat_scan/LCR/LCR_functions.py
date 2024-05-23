# imports
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import xarray as xr
import os
import pandas as pd
import numpy as np

from heat_scan.tools.pangeo_CMIP import pangeo_CMIP_funs
from heat_scan.tools import constants
from heat_scan.tools.polygons import polygon_funs
from heat_scan.LCR import LCR_functions

import matplotlib

matplotlib.use('TkAgg')


def define_study_cities(current_dir=os.getcwd().replace('\\', '/') + '/', plot=False):
    """
    CSV with city choices manually created.
    ChatGPT asked to pull 100 cities with largest population in LCR.
    ChatGPT asked to produce rough coordinates for these cities.
    These are saved in csv file city_coords.csv.
    These are read in here as geo df.

    :return city_coords_gdf: GeoDataFrame of study cities.
    """

    # ToDo: populate this csv with more than one city.
    # refer to the draft report, and the UHI study in LCR paper etc.

    # read in the city csv
    city_coord_file_path = current_dir + 'UN_2015_cities_over_300k.csv'

    # confirm the file exists
    assert os.path.isfile(city_coord_file_path)

    city_coords = pd.read_csv(city_coord_file_path)

    geometry = [Point(xy) for xy in zip(city_coords.longitude, city_coords.latitude)]
    city_coords = city_coords.drop(['longitude', 'latitude'], axis=1)
    city_coords_gdf = gpd.GeoDataFrame(city_coords, crs="EPSG:4326", geometry=geometry)

    return city_coords_gdf


def days_over_threshold(data_dict, threshold, year, source_id, **kwargs):
    """

    :return:
    """
    # ToDo: Docstring here

    print(' ')

    days_list = []

    for country in data_dict:

        print(country)

        # check to see if file already exists

        if type(year) == list:
            year_label = str(year[0]) + '_to_' + str(year[-1])
        else:
            assert type(year) == int
            year_label = str(year)

        current_dir = os.getcwd().replace('\\', '/') + '/'
        csv_dir = current_dir + 'stats_countries/' + year_label + '/'
        assert os.path.exists(csv_dir)

        this_filename = country + '_' + source_id + '_' + kwargs['experiment_id'] + '.csv'

        if os.path.isfile(csv_dir + this_filename):

            # the file exists, read the file
            df = pd.read_csv(csv_dir + this_filename)

            days_list.append(df)

        else:

            ds = data_dict[country]
            high_vals = xr.where(ds.tasmax > threshold, 1, 0)  # set all temps over threshold = 1; others to 0
            summed_vals = high_vals.sum(dim='time')

            # replace any 0 values with nan
            summed_vals = summed_vals.where(summed_vals > 0)

            if type(year) == list:
                summed_vals = summed_vals / len(year)

            summed_vals = summed_vals.compute()

            mean_val = np.nanmean(summed_vals)
            max_val = np.nanmax(summed_vals)
            min_val = np.nanmin(summed_vals)
            median_val = np.nanmedian(summed_vals)

            mean_temp = np.nanmean(summed_vals)
            max_temp = np.nanmax(summed_vals)
            min_temp = np.nanmin(summed_vals)
            median_temp = np.nanmedian(summed_vals)

            df_dict = {'Country': [country], 'Mean days': [mean_val], 'Median days': [median_val],
                       'Max days': [max_val],
                       'Min days': [min_val],
                       'Mean temp': [mean_temp], 'Median temp': [median_temp], 'Max temp': [max_temp],
                       'Min temp': [min_temp]}

            df = pd.DataFrame.from_dict(df_dict)

            df.to_csv(csv_dir + this_filename)

            days_list.append(df)

    combined_df = pd.concat(days_list)

    combined_df.index = combined_df.Country
    combined_df = combined_df.drop(columns=['Country'])

    if 'Unnamed: 0' in combined_df.columns:
        combined_df = combined_df.drop(columns=['Unnamed: 0'])

    return combined_df


def days_over_threshold_stats(ds, polygon_df, threshold, year, source_id, test=False, plot=False, **kwargs):
    """

    :return:
    """
    # ToDo: docstring here

    if test:
        test_flag = '_test'
    else:
        test_flag = ''

    assert len(list(ds.keys())) == 1
    var_name = list(ds.keys())[0]

    data_dict = polygon_funs.select_data_in_multiple_country_polygons(array=ds[var_name], polygon_df=polygon_df,
                                                                      plot=plot, year=year, **kwargs)

    df = days_over_threshold(data_dict=data_dict,
                             threshold=threshold + constants.convert_kelvin, year=year, source_id=source_id,
                             **kwargs)

    # save combined csv
    if type(year) == list:
        year_label = str(year[0]) + '_to_' + str(year[-1])
    else:
        assert type(year) == int
        year_label = str(year)

    df.to_csv(os.getcwd().replace('\\', '/') + '/' + year_label + '_days_over_' + str(threshold) + '_' + source_id + test_flag + '.csv')

    print('end')
