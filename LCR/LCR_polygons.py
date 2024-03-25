# imports
import os
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import xarray as xr
import gcsfs

import matplotlib

matplotlib.use('TkAgg')


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


def cmip6_via_pangeo(plot=False):
    """
    Alternative way (to CCKP) of getting CMIP6 data: Suggested by Matthias.
    Analysis of Google Cloud CMIP6 data using Pangeo tools.
    instruction: https://medium.com/pangeo/cmip6-in-the-cloud-five-ways-96b177abe396
    variable name table: https://pcmdi.llnl.gov/mips/cmip3/variableList.html#Table_A1f
    Link to pangeo-cmip6.csv: https://cmip6.storage.googleapis.com/pangeo-cmip6.csv

    :return:
    """

    # link provided by Matthias
    # last number, e.g. "20170706" is variable code, listed in the included pangeo-cmip6.csv file, and identified
    # using the table from the link:
    # https://pcmdi.llnl.gov/mips/cmip3/variableList.html#Table_A1f
    zstore = "gs://cmip6/CMIP6/HighResMIP/CMCC/CMCC-CM2-HR4/highresSST-present/r1i1p1f1/Amon/tas/gn/v20170706/"

    fs = gcsfs.GCSFileSystem(token='anon', access='read_only')
    mapper = fs.get_mapper(zstore)

    # open it using xarray and zarr
    ds = xr.open_zarr(mapper, consolidated=True)

    # change lon from degrees east to between -180 to 180
    ds.coords['lon'] = (ds.coords['lon'] + 180) % 360 - 180
    ds = ds.sortby(ds.lon)

    if plot:
        # To plot the first time step
        ds.tas.isel(time=0).plot()

    return ds


if __name__ == "__main__":
    # define global city boundaries
    polygon_df = global_city_boundaries()

    # define study cities
    city_coords_gdf = define_study_cities()

    # pull the polygon that the city coord is in

    # TEST CASE
    # ToDo: don't just call 1 point.
    point = city_coords_gdf.iloc[0].geometry

    closest_polygon = coord_polygon_overlap(point, polygon_df)

    # grab CMIP6 data
    ds = cmip6_via_pangeo()

    # check w/ data: fig
    fig = plt.figure(figsize=(8, 7))
    ax = plt.subplot(1, 1, 1)
    ds.tas.isel(time=0).plot(ax=ax)
    polygon_df.plot(ax=ax)
    gpd.GeoSeries([closest_polygon]).plot(ax=ax, facecolor='r')
    ax.scatter(point.x, point.y, c='k')

    print('end')
