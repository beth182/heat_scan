import os
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import matplotlib.pyplot as plt

current_dir = os.getcwd().replace('\\', '/') + '/'

poly_file_path = current_dir + 'city_polygons/GHS_SDATA_WUP2018_BOUNDARIES_MT_GLOBE_R2023A_V1_0.shp'

# confirm the file exists
assert os.path.isfile(poly_file_path)

polygon_df = gpd.read_file(poly_file_path)

# get rid of invalid lines
# polygon_df = polygon_df.loc[polygon_df.geometry.is_valid]

# polygon_df.plot()


# read in the city csv
city_coord_file_path = current_dir + 'city_coords.csv'

# confirm the file exists
assert os.path.isfile(city_coord_file_path)

city_coords = pd.read_csv(city_coord_file_path)

geometry = [Point(xy) for xy in zip(city_coords.Lon, city_coords.Lat)]
city_coords = city_coords.drop(['Lon', 'Lat'], axis=1)
city_coords_gdf = gpd.GeoDataFrame(city_coords, crs="EPSG:4326", geometry=geometry)

# plt.scatter(city_coords.Lon[0], city_coords.Lat[0])

# pull the polygon that the city coord is in
point = city_coords_gdf.iloc[0].geometry

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
    print('end')

# check w/ plot
# gpd.GeoSeries([closest_polygon]).plot()
# plt.scatter(point.x, point.y, c='r')



# check w/ data

import xarray as xr
import gcsfs

# Analysis of Google Cloud CMIP6 data using Pangeo tools.

# instruction: https://medium.com/pangeo/cmip6-in-the-cloud-five-ways-96b177abe396
# variable name table: https://pcmdi.llnl.gov/mips/cmip3/variableList.html#Table_A1f
# Link to pangeo-cmip6.csv: https://cmip6.storage.googleapis.com/pangeo-cmip6.csv

current_dir = os.getcwd().replace('\\', '/') + '/'

zstore = "gs://cmip6/CMIP6/HighResMIP/CMCC/CMCC-CM2-HR4/highresSST-present/r1i1p1f1/Amon/tas/gn/v20170706/"

fs = gcsfs.GCSFileSystem(token='anon', access='read_only')
mapper = fs.get_mapper(zstore)

# open it using xarray and zarr
ds = xr.open_zarr(mapper, consolidated=True)

# change lon from degrees east to between -180 to 180
ds.coords['lon'] = (ds.coords['lon'] + 180) % 360 - 180
ds = ds.sortby(ds.lon)

# To plot the first time step
# ds.tas.isel(time=0).plot()


print('end')

# fig
fig = plt.figure(figsize=(8, 7))
ax = plt.subplot(1, 1, 1)
ds.tas.isel(time=0).plot(ax=ax)
polygon_df.plot(ax=ax)
gpd.GeoSeries([closest_polygon]).plot(ax=ax, facecolor='r')
ax.scatter(point.x, point.y, c='k')
