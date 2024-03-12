import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, MultiPolygon
import fiona

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

if min_distance == 0:
    print('end')

# check w/ plot
# gpd.GeoSeries([closest_polygon]).plot()
# plt.scatter(point.x, point.y, c='r')
