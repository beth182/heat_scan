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
test = True

country_shapes = polygon_funs.global_country_boundaries()
country_df = polygon_funs.select_country_boundaries(country_shapes, countries_list)

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
                                 member_id='r1i1p1f1', grid_label='gn', country_df=country_df,
                                 day_threshold_stats=True, test=test)
