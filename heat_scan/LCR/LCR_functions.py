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
    city_coord_file_path = current_dir + 'city_coords.csv'

    # confirm the file exists
    assert os.path.isfile(city_coord_file_path)

    city_coords = pd.read_csv(city_coord_file_path)

    geometry = [Point(xy) for xy in zip(city_coords.Lon, city_coords.Lat)]
    city_coords = city_coords.drop(['Lon', 'Lat'], axis=1)
    city_coords_gdf = gpd.GeoDataFrame(city_coords, crs="EPSG:4326", geometry=geometry)

    # sanity plot
    if plot:
        plt.scatter(city_coords.Lon[0], city_coords.Lat[0])
        plt.show()

    return city_coords_gdf


def days_over_threshold(data_dict, threshold, year):
    """

    :return:
    """
    # ToDo: Docstring here

    days_dict = {}
    for country in data_dict:
        ds = data_dict[country]
        high_vals = xr.where(ds > threshold, 1, 0)  # set all temps over threshold = 1; others to 0
        summed_vals = high_vals.sum(dim='time')

        # replace any 0 values with nan
        summed_vals = summed_vals.where(summed_vals > 0)

        if type(year) == list:
            summed_vals = summed_vals / len(year)

        days_dict[country] = summed_vals

    return days_dict


def days_over_threshold_stats(ds, polygon_df, threshold, year, source_id, test=False, plot=False):
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
                                                                      plot=plot)

    day_count_dict = days_over_threshold(data_dict=data_dict,
                                         threshold=threshold + constants.convert_kelvin, year=year)

    mean_vals = []
    max_vals = []
    min_vals = []
    median_vals = []

    mean_temp = []
    max_temp = []
    min_temp = []
    median_temp = []

    countries_list = polygon_df.shapeName.to_list()

    for country in countries_list:
        mean_vals.append(np.nanmean(day_count_dict[country]))
        max_vals.append(np.nanmax(day_count_dict[country]))
        min_vals.append(np.nanmin(day_count_dict[country]))
        median_vals.append(np.nanmedian(day_count_dict[country]))

        mean_temp.append(np.nanmean(data_dict[country]))
        max_temp.append(np.nanmax(data_dict[country]))
        min_temp.append(np.nanmin(data_dict[country]))
        median_temp.append(np.nanmedian(data_dict[country]))

    df_dict = {'Country': countries_list, 'Mean days': mean_vals, 'Median days': median_vals, 'Max days': max_vals,
               'Min days': min_vals,
               'Mean temp': mean_temp, 'Median temp': median_temp, 'Max temp': max_temp, 'Min temp': min_temp}
    df = pd.DataFrame.from_dict(df_dict)

    if type(year) == list:
        year_label = str(year[0]) + '_to_' + str(year[-1])
    else:
        assert type(year) == int
        year_label = str(year)

    df.to_csv(os.getcwd().replace('\\', '/') + '/' + year_label + '_days_over_' + str(
        threshold) + '_' + source_id + test_flag + '.csv')
