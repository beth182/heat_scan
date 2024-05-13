# imports
import os
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import numpy as np
import rasterio as rio
from rasterio import features as feat
from mpl_toolkits.basemap import Basemap
import xarray as xr

import matplotlib

matplotlib.use('TkAgg')

from heat_scan.tools.pangeo_CMIP import pangeo_CMIP_funs
from heat_scan.tools import constants


def read_boundary_shapefile(poly_file_path, plot=False):
    """

    :param poly_file_path:
    :param plot:
    :return:
    """
    # ToDo: Docstring here

    # confirm the file exists
    assert os.path.isfile(poly_file_path)

    polygon_df = gpd.read_file(poly_file_path)

    # get rid of invalid lines
    # polygon_df = polygon_df.loc[polygon_df.geometry.is_valid]

    # plot to check
    if plot:
        polygon_df.plot()
        plt.show()

    return polygon_df


def global_city_boundaries(current_dir=os.getcwd().replace('\\', '/') + '/', plot=False):
    """
    Global city polygon boundaries
    City boundaries of the UN World Urbanization Prospects 2018 city database
    pre-downloaded to city_polygons folder using the link:
    https://ghsl.jrc.ec.europa.eu/download.php?ds=sdata
    documentation existing in the report at link:
    https://ghsl.jrc.ec.europa.eu/documents/GHSL_Data_Package_2023.pdf?t=1698413418

    :return polygon_df: GeoDataFrame of global city boundaries as polygons.
    """

    poly_file_path = current_dir + 'city_polygons/GHS_SDATA_WUP2018_BOUNDARIES_MT_GLOBE_R2023A_V1_0.shp'

    polygon_df = read_boundary_shapefile(poly_file_path, plot)

    return polygon_df


def global_country_boundaries(current_dir=os.getcwd().replace('\\', '/') + '/', plot=False):
    """
    https://www.geoboundaries.org/countryDownloads.html
    :return:
    """
    # ToDo: Docstring here

    poly_file_path = current_dir + '../tools/geoBoundaries/countries/geoBoundariesCGAZ_ADM0.shp'

    polygon_df = read_boundary_shapefile(poly_file_path, plot)

    return polygon_df


def select_country_boundaries(polygon_df, country_name_list, plot=False):
    """

    :param country_name_list:
    :return:
    """
    # ToDo: Docstring here

    country_row_list = []
    for name in country_name_list:

        try:
            assert name in polygon_df.shapeName.to_list()
        except:
            print('end')

        country_row = polygon_df[polygon_df.shapeName == name]
        country_row_list.append(country_row)

    country_df = pd.concat(country_row_list)

    # plot to check
    if plot:
        country_df.plot()
        m = Basemap()
        m.drawcoastlines()
        m.drawcountries()
        plt.show()

    return country_df


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


def coord_polygon_overlap(point, polygon_df, plot=False):
    """
    Find the overlap between a given coordinate (point geometry) and a GeoDataFrame of polygons.
    NOTE: if distance between coord and polygon is bigger than zero, process is stopped.
    :return closest_polygon: Closest polygon in a GeoDataFrame to a given point coord.
    """

    min_distance = float('inf')
    closest_polygon = None

    distances = []

    for index, row in polygon_df.iterrows():
        distance = point.distance(row['geometry'])
        distances.append(distance)

        if distance < min_distance:
            min_distance = distance
            closest_polygon = row['geometry']

    if min_distance != 0:
        # ToDo: eventually rm this
        print('end')

    assert min_distance == 0

    if plot:
        # sanity check
        gpd.GeoSeries([closest_polygon]).plot()
        plt.scatter(point.x, point.y, c='r')

    return closest_polygon


def select_data_in_multiple_country_polygons(array, polygon_df, plot=False):
    """

    :return:
    """
    # ToDo: Docstring here

    data_dict = {}

    count = 1
    for index, row in polygon_df.iterrows():
        print(str(count) + '/' + str(len(polygon_df)) + ': ' + row.shapeName)
        data_dict[row.shapeName] = select_data_in_polygon(array, row, plot=plot, country=row.shapeName)
        count += 1

    return data_dict


def select_data_in_polygon(array, polygon, plot=False, **kwargs):
    """
    Function which grabs the data overlapping with a city boundary
    :return:
    """

    # Create a mask of the polygon
    transform = rio.transform.from_bounds(array.lon[0], array.lat[-1], array.lon[-1], array.lat[0],
                                          array.shape[2], array.shape[1])

    mask = feat.geometry_mask([polygon.geometry],
                              out_shape=(array.shape[1], array.shape[2]),
                              transform=transform,
                              all_touched=True,
                              invert=True)

    # Apply the spatial mask across all times
    masked_data = array.where(mask)

    if plot:
        # check w/ data: fig
        fig = plt.figure(figsize=(8, 7))
        ax = plt.subplot(1, 1, 1)
        masked_data.isel(time=0).plot(ax=ax, zorder=1)
        gpd.GeoSeries([polygon.geometry]).plot(ax=ax, facecolor='r', zorder=2)
        # ax.scatter(point.x, point.y, c='k')
        assert 'country' in kwargs.keys()
        plt.savefig(os.getcwd().replace('\\', '/') + '/country_boundary_tests/' + kwargs['country'] + '.png', bbox_inches='tight', dpi=300)

    # Now `masked_data` contains only the values within or touching the polygon.
    return masked_data


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


if __name__ == "__main__":
    # ToDo: add proper function for this
    # ToDo: have a global country csv file - with continents (regions) included
    # READ IN COUNTRY NAME FILE
    # made from copying info from https://www.worldometers.info/geography/how-many-countries-in-latin-america/

    # LCR_countries = pd.read_csv(os.getcwd().replace('\\', '/') + '/countries_in_LCR.csv')
    # countries_list = LCR_countries.Country.to_list()
    # test = False

    test_countries = pd.read_csv(os.getcwd().replace('\\', '/') + '/countries_in_test.csv')
    countries_list = test_countries.Country.to_list()

    country_shapes = global_country_boundaries()
    country_df = select_country_boundaries(country_shapes, countries_list)
    test = True

    """
    # define global city boundaries
    polygon_df = global_city_boundaries()

    # define study cities
    city_coords_gdf = define_study_cities()

    # pull the polygon that the city coord is in

    # TEST CASE
    # ToDo: don't just call 1 point.
    point = city_coords_gdf.iloc[0].geometry

    closest_polygon = coord_polygon_overlap(point, polygon_df)

    # some bs
    if closest_polygon.type == 'MultiPolygon':
        polylist = list(closest_polygon.geoms)
        closest_polygon = polylist[0]
    """

    # grab CMIP6 data
    # year = 2015
    year = 2050
    # year = 2100
    experiment_id = 'ssp245'

    # defult ESM4 run
    # source_id = 'GFDL-ESM4'
    # ds = pangeo_CMIP_funs.main_find_CMIP(variable_id='tasmax', experiment_id=experiment_id, year=year)

    source_id = 'ACCESS-CM2'
    ds = pangeo_CMIP_funs.main_find_CMIP(variable_id = 'tasmax', experiment_id=experiment_id, year=year, institution_id='CSIRO-ARCCSS', source_id=source_id, member_id='r1i1p1f1', grid_label='gn')

    if test:
        test_flag = '_test'
    else:
        test_flag = ''


    assert len(list(ds.keys())) == 1
    var_name = list(ds.keys())[0]

    data_dict = select_data_in_multiple_country_polygons(array=ds[var_name], polygon_df=country_df,plot=False)

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

    df_dict = {'Country': countries_list, 'Mean days': mean_vals, 'Median days': median_vals, 'Max days': max_vals, 'Min days': min_vals,
               'Mean temp': mean_temp, 'Median temp': median_temp, 'Max temp': max_temp, 'Min temp': min_temp}
    df = pd.DataFrame.from_dict(df_dict)
    df.to_csv(os.getcwd().replace('\\', '/') + '/' + str(year) + '_days_over_' + str(threshold) + '_' + source_id + test_flag + '.csv')

    print('end')
