import xarray as xr
import numpy as np

from mpl_toolkits.basemap import Basemap, maskoceans
import matplotlib.pyplot as plt
from matplotlib.patches import Path, PathPatch
import matplotlib

matplotlib.use('TkAgg')

from heat_scan.tools import pangeo_CMIP_funs
from heat_scan.tools import constants

# tasmax
# r1i1p1f1
# NOAA-GFDL
# ScenarioMIP
# ssp245
# day
zstore = 'gs://cmip6/CMIP6/ScenarioMIP/NOAA-GFDL/GFDL-ESM4/ssp245/r1i1p1f1/day/tasmax/gr1/v20180701/'

ds = pangeo_CMIP_funs.cmip6_via_pangeo(zstore=zstore)

# plot data

fig, ax = plt.subplots(1, figsize=(12, 12))
deg_c = ds.tasmax.isel(time=0) + constants.convert_kelvin
deg_c.plot(ax=ax)
m = Basemap()
m.drawcoastlines()

# making the ocean white
# getting the limits of the map:
x0, x1 = ax.get_xlim()
y0, y1 = ax.get_ylim()
map_edges = np.array([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])
# getting all polygons used to draw the coastlines of the map
polys = [p.boundary for p in m.landpolygons]
# combining with map edges
polys = [map_edges] + polys[:]
# creating a PathPatch
codes = [
    [Path.MOVETO] + [Path.LINETO for p in p[1:]]
    for p in polys
]
polys_lin = [v for p in polys for v in p]
codes_lin = [c for cs in codes for c in cs]
path = Path(polys_lin, codes_lin)
patch = PathPatch(path, facecolor='white', lw=0)
# masking the data:
ax.add_patch(patch)

print('end')
