# imports
import os
import pandas as pd
import numpy as np

from heat_scan.tools.pangeo_CMIP import pangeo_CMIP_funs
from heat_scan.tools import constants
from heat_scan.tools.polygons import polygon_funs
from heat_scan.LCR import LCR_functions

"""
# define global city boundaries
polygon_df = polygon_funs.global_city_boundaries()

# define study cities
city_coords_gdf = LCR_functions.define_study_cities()

# pull the polygon that the city coord is in

# TEST CASE
# ToDo: don't just call 1 point.
point = city_coords_gdf.iloc[0].geometry

closest_polygon = polygon_funs.coord_polygon_overlap(point, polygon_df)

# some bs
if closest_polygon.type == 'MultiPolygon':
 polylist = list(closest_polygon.geoms)
 closest_polygon = polylist[0]
 """

# user inputs


# ToDo: add proper function for this
# ToDo: have a global country csv file - with continents (regions) included
# READ IN COUNTRY NAME FILE
# made from copying info from https://www.worldometers.info/geography/how-many-countries-in-latin-america/

# LCR_countries = pd.read_csv(os.getcwd().replace('\\', '/') + '/countries_in_LCR.csv')
# countries_list = LCR_countries.Country.to_list()
# test = False

test_countries = pd.read_csv(os.getcwd().replace('\\', '/') + '/countries_in_test.csv')
countries_list = test_countries.Country.to_list()

country_shapes = polygon_funs.global_country_boundaries()
country_df = polygon_funs.select_country_boundaries(country_shapes, countries_list)
test = True

# grab CMIP6 data
# year = 2015
year = 2050
# year = 2100
experiment_id = 'ssp245'

# defult ESM4 run
# source_id = 'GFDL-ESM4'
# ds = pangeo_CMIP_funs.main_find_CMIP(variable_id='tasmax', experiment_id=experiment_id, year=year)

source_id = 'ACCESS-CM2'
# ds = pangeo_CMIP_funs.main_find_CMIP(variable_id = 'tasmax', experiment_id=experiment_id, year=year, institution_id='CSIRO-ARCCSS', source_id=source_id, member_id='r1i1p1f1', grid_label='gn')


# pangeo_CMIP_funs.run_projections(threshold=30, variable_id='tasmax', experiment_id=experiment_id, year=year, region='LCR')
pangeo_CMIP_funs.run_projections(variable_id='tasmax', threshold=30, experiment_id=experiment_id, year=year,
                                 region='LCR', institution_id='CSIRO-ARCCSS', source_id='ACCESS-CM2',
                                 member_id='r1i1p1f1', grid_label='gn')

if test:
    test_flag = '_test'
else:
    test_flag = ''

assert len(list(ds.keys())) == 1
var_name = list(ds.keys())[0]

data_dict = select_data_in_multiple_country_polygons(array=ds[var_name], polygon_df=country_df, plot=False)

threshold = 30
day_count_dict = days_over_threshold(data_dict=data_dict, threshold=threshold + constants.convert_kelvin)

mean_vals = []
max_vals = []
min_vals = []
median_vals = []

mean_temp = []
max_temp = []
min_temp = []
median_temp = []

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
df.to_csv(os.getcwd().replace('\\', '/') + '/' + str(year) + '_days_over_' + str(
    threshold) + '_' + source_id + test_flag + '.csv')
