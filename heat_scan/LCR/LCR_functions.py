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

import matplotlib

matplotlib.use('TkAgg')

from heat_scan.tools.pangeo_CMIP import pangeo_CMIP_funs


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


def select_data(ds, closest_polygon, plot=False):
    """
    Function which grabs the data overlapping with a city boundary
    :return:
    """

    assert len(list(ds.keys())) == 1
    var_name = list(ds.keys())[0]

    # ToDo: think about the time selection
    # for now just use the first time
    array = ds.tas.isel(time=0)

    # Create a grid representing the dataset
    grid_lons, grid_lats = np.meshgrid(array.lon, array.lat)

    # Create a mask of the polygon
    transform = rio.transform.from_bounds(array.lon[0], array.lat[-1], array.lon[-1], array.lat[0],
                                          array.shape[1], array.shape[0])
    mask = feat.geometry_mask([closest_polygon],
                              out_shape=(array.shape[0], array.shape[1]),
                              transform=transform,
                              all_touched=True,
                              invert=True)

    # Apply the mask to the xarray dataset
    masked_data = array.where(mask)

    if plot:
        # check w/ data: fig
        fig = plt.figure(figsize=(8, 7))
        ax = plt.subplot(1, 1, 1)
        masked_data.plot(ax=ax)
        polygon_df.plot(ax=ax)
        gpd.GeoSeries([closest_polygon]).plot(ax=ax, facecolor='r')
        # ax.scatter(point.x, point.y, c='k')

    # Now `masked_data` contains only the values within or touching the polygon.
    return masked_data


if __name__ == "__main__":

    # ToDo: add proper function for this
    # ToDo: have a global country csv file - with continents (regions) included
    # READ IN COUNTRY NAME FILE
    # made from copying info from https://www.worldometers.info/geography/how-many-countries-in-latin-america/
    LCR_countries = pd.read_csv(os.getcwd().replace('\\', '/') + '/countries_in_LCR.csv')
    LCR_countries_list = LCR_countries.Country.to_list()

    country_shapes = global_country_boundaries()
    country_df = select_country_boundaries(country_shapes, LCR_countries_list)

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
    year = 2015
    experiment_id = 'ssp245'
    ds = pangeo_CMIP_funs.main_find_CMIP(variable_id = 'tasmax', experiment_id=experiment_id, year=year)

    masked_data = select_data(ds, closest_polygon)

    val = np.nanmean(masked_data)

    print('end')
