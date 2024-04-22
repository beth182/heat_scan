from heat_scan.LCR import LCR_functions
from mpl_toolkits.basemap import Basemap,maskoceans
import matplotlib.pyplot as plt

import xarray as xr
import numpy as np








# tasmax
# r1i1p1f1
# NOAA-GFDL
# ScenarioMIP
# ssp245
# day
zstore = 'gs://cmip6/CMIP6/ScenarioMIP/NOAA-GFDL/GFDL-ESM4/ssp245/r1i1p1f1/day/tasmax/gr1/v20180701/'

ds = LCR_functions.cmip6_via_pangeo(zstore=zstore)

fig, ax = plt.subplots(1, figsize=(12, 12))
ds.tasmax.isel(time=0).plot(ax=ax)
m = Basemap()
m.drawcoastlines()



print('end')


