import os

from heat_scan.tools import pangeo_CMIP_funs
from heat_scan.tools import constants
from heat_scan.transport import plotting_funs

save_path = os.getcwd().replace('\\', '/') + '/'

# tasmax
# r1i1p1f1
# NOAA-GFDL
# ScenarioMIP
# ssp245
# day
zstore = 'gs://cmip6/CMIP6/ScenarioMIP/NOAA-GFDL/GFDL-ESM4/ssp245/r1i1p1f1/day/tasmax/gr1/v20180701/'

ds = pangeo_CMIP_funs.cmip6_via_pangeo(zstore=zstore)

# plot data
# straight variable at a given time
# plotting_funs.plt_straight_variable(ds, 210)


# Count of days where variable is over a given threshold

# get data from a given year
year = 2050
ds_2015 = ds.sel(time=ds.time.dt.year.isin([year]))

# define threshold
threshold_temp = 30 + constants.convert_kelvin

plotting_funs.plt_count_over_threshold(ds=ds_2015, threshold=threshold_temp, year=year, save_path=save_path)

print('end')
