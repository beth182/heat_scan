import pandas as pd
import xarray as xr
import gcsfs
import matplotlib.pyplot as plt
import os
from shapely.geometry import Point
import geopandas as gpd

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


# grab data for desired coord
# test cood
# read in the city csv
city_coord_file_path = current_dir + 'city_coords.csv'
# confirm the file exists
assert os.path.isfile(city_coord_file_path)
city_coords = pd.read_csv(city_coord_file_path)
geometry = [Point(xy) for xy in zip(city_coords.Lon, city_coords.Lat)]
city_coords = city_coords.drop(['Lon', 'Lat'], axis=1)
city_coords_gdf = gpd.GeoDataFrame(city_coords, crs="EPSG:4326", geometry=geometry)

point = city_coords_gdf.iloc[0].geometry
plt.scatter(point.x + 360, point.y, c='r')

print('end')
