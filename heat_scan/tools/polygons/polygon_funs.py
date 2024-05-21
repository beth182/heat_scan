# imports
import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import rasterio as rio
from rasterio import features as feat
from mpl_toolkits.basemap import Basemap
import xarray as xr

import matplotlib

matplotlib.use('TkAgg')


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

    poly_file_path = current_dir + '../tools/polygons/city_polygons/GHS_SDATA_WUP2018_BOUNDARIES_MT_GLOBE_R2023A_V1_0.shp'

    polygon_df = read_boundary_shapefile(poly_file_path, plot)

    return polygon_df


def global_country_boundaries(current_dir=os.getcwd().replace('\\', '/') + '/', plot=False):
    """
    https://www.geoboundaries.org/countryDownloads.html
    :return:
    """
    # ToDo: Docstring here

    poly_file_path = current_dir + '../tools/polygons/geoBoundaries/countries/geoBoundariesCGAZ_ADM0.shp'

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


def select_data_in_multiple_country_polygons(array, polygon_df, plot=False, **kwargs):
    """

    :return:
    """
    # ToDo: Docstring here

    data_dict = {}

    count = 1
    for index, row in polygon_df.iterrows():
        print(str(count) + '/' + str(len(polygon_df)) + ': ' + row.shapeName)
        data_dict[row.shapeName] = select_data_in_polygon(array, row, plot=plot, country=row.shapeName, **kwargs)
        count += 1

    return data_dict


def create_mask(polygon, array):
    # Create a mask of the polygon
    transform = rio.transform.from_bounds(array.lon[0], array.lat[-1], array.lon[-1], array.lat[0],
                                          array.shape[-1], array.shape[-2])
    mask = feat.geometry_mask([polygon.geometry],
                              out_shape=(array.shape[-2], array.shape[-1]),
                              transform=transform,
                              all_touched=True,
                              invert=True)

    return mask


def apply_mask(array, mask):
    # Apply the spatial mask across all times using vectorized operations
    mask_expanded = mask[None, :, :]  # Add a new axis for time dimension
    return array.where(mask_expanded)


def select_data_in_polygon(array, polygon, plot=False, **kwargs):
    """
    Function which grabs the data overlapping with a city boundary
    :return:
    """

    # Create mask
    mask = create_mask(polygon, array)

    # Apply mask
    masked_data = apply_mask(array, mask)

    # export country data as netcdf
    if 'source_id' in kwargs.keys():
        source_id = kwargs['source_id']
    else:
        source_id = 'GFDL-ESM4'

    current_dir = os.getcwd().replace('\\', '/') + '/'
    assert os.path.exists(current_dir + 'netCDF_countries/')
    masked_data.compute().to_netcdf(
        current_dir + 'netCDF_countries/' + kwargs['country'] + '_' + source_id + '_' + kwargs['experiment_id'] + '.nc')

    if plot:
        # check w/ data: fig
        fig = plt.figure(figsize=(8, 7))
        ax = plt.subplot(1, 1, 1)
        masked_data.isel(time=0).plot(ax=ax, zorder=1)
        gpd.GeoSeries([polygon.geometry]).plot(ax=ax, facecolor='r', zorder=2)
        # ax.scatter(point.x, point.y, c='k')
        assert 'country' in kwargs.keys()
        plt.savefig(os.getcwd().replace('\\', '/') + '/country_boundary_tests/' + kwargs['country'] + '.png',
                    bbox_inches='tight', dpi=300)

    # Now `masked_data` contains only the values within or touching the polygon.
    return masked_data


def get_country_df(csv_dir=os.getcwd().replace('\\', '/'), test=False, **kwargs):
    """
    region: as string. Can be test, global, or region e.g. LCR
    LCR country csv made from copying info from https://www.worldometers.info/geography/how-many-countries-in-latin-america/
    :return:
    """
    # ToDo: docstring here
    # ToDo: have a global country csv file - with continents (regions) included

    if test:
        region = 'test'
    else:
        assert 'region' in kwargs.keys()
        region = kwargs['region']

    # csv path
    csv_path = csv_dir + '/countries_in_' + region + '.csv'
    assert os.path.isfile(csv_path)

    countries = pd.read_csv(csv_path)
    countries_list = countries.Country.to_list()

    country_shapes = global_country_boundaries()
    country_df = select_country_boundaries(country_shapes, countries_list)

    return country_df
