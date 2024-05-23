# imports
import os
import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import matplotlib
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

matplotlib.use('TkAgg')

from heat_scan.LCR import LCR_functions
from heat_scan.tools.polygons import polygon_funs
from heat_scan.tools import constants


def select_data_in_city(array, polygon):
    """

    :return:
    """
    # ToDo: docstring here
    # ToDo: move to polygon funs

    # Create mask
    mask = polygon_funs.create_mask(polygon, array)

    # Apply mask
    masked_data = polygon_funs.apply_mask(array, mask)

    return masked_data


# user inputs
# year = list(range(2015, 2026))
# year = list(range(2040, 2051))
year = list(range(2090, 2101))

source_id = 'GFDL-ESM4'
experiment_id = 'ssp245'
threshold = 30

# define global city boundaries
polygon_df = polygon_funs.global_city_boundaries()

# define study cities
city_coords_gdf = LCR_functions.define_study_cities()

# pull the polygon that the city coord is in

# TEST CASE
# ToDo: don't just call 1 point.

df_list = []

# iterate over the gdf
count = 1
for index, row in city_coords_gdf.iterrows():

    country = row.Country
    city = row.City
    point = row.geometry

    print(city + ', ' + country + ': ' + str(count) + '/' + str(len(city_coords_gdf)))



    closest_polygon = polygon_funs.coord_polygon_overlap(point, polygon_df, plot=False)

    # some bs
    if closest_polygon.type == 'MultiPolygon':
        polylist = list(closest_polygon.geoms)
        closest_polygon = polylist[0]

    if type(year) == list:
        year_label = str(year[0]) + '_to_' + str(year[-1])
    else:
        assert type(year) == int
        year_label = str(year)

    # find the nc file for the country
    current_dir = os.getcwd().replace('\\', '/') + '/'
    nc_file_dir = current_dir + 'netCDF_countries/' + year_label + '/'
    nc_file_name = country + '_' + source_id + '_' + experiment_id + '.nc'

    nc_file_path = nc_file_dir + nc_file_name
    # make sure the file exists
    try:
        assert os.path.isfile(nc_file_path)
    except:
        print('end')

    # read data for country
    country_data = xr.open_dataset(nc_file_path)

    # if plot
    # country_data.tasmax.isel(time=0).plot.imshow()
    # gpd.GeoSeries([closest_polygon]).plot()
    # plt.scatter(point.x, point.y, c='r')

    masked_data = select_data_in_city(array=country_data['tasmax'], polygon=closest_polygon)

    high_vals = xr.where(masked_data > threshold + constants.convert_kelvin, 1, 0)  # set all temps over threshold = 1; others to 0
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

    df_dict = {'City': [city], 'Country': [country], 'Mean days': [mean_val], 'Median days': [median_val],
               'Max days': [max_val],
               'Min days': [min_val],
               'Mean temp': [mean_temp], 'Median temp': [median_temp], 'Max temp': [max_temp],
               'Min temp': [min_temp]}

    df = pd.DataFrame.from_dict(df_dict)
    df_list.append(df)
    count += 1



df_all = pd.concat(df_list)

df_all.to_csv(current_dir + 'cities_' + year_label + '_' + source_id + '_' + experiment_id + '.csv')

print('end')
