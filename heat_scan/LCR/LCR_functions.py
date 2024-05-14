# imports
import os
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import xarray as xr

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


def days_over_threshold(data_dict, threshold):
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

        days_dict[country] = summed_vals

    return days_dict
