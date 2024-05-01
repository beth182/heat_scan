import os

from heat_scan.tools.pangeo_CMIP import pangeo_CMIP_funs
from heat_scan.tools import constants
from heat_scan.transport import plotting_funs


def main_find_CMIP(year=None):
    """

    :param save_path:
    :return:
    """
    # ToDo: function to search the csv for user's choices here

    # where the zstore is returned

    # tasmax
    # r1i1p1f1
    # NOAA-GFDL
    # ScenarioMIP
    # ssp245
    # day
    zstore = 'gs://cmip6/CMIP6/ScenarioMIP/NOAA-GFDL/GFDL-ESM4/ssp245/r1i1p1f1/day/tasmax/gr1/v20180701/'
    # zstore = 'gs://cmip6/CMIP6/ScenarioMIP/NOAA-GFDL/GFDL-ESM4/ssp585/r1i1p1f1/day/tasmax/gr1/v20180701/'

    # zstore = 'gs://cmip6/CMIP6/ScenarioMIP/CCCma/CanESM5/ssp245/r1i1p2f1/day/tasmax/gn/v20190429/'

    # zstore = 'gs://cmip6/CMIP6/ScenarioMIP/BCC/BCC-CSM2-MR/ssp245/r1i1p1f1/day/tasmax/gn/v20190318/'

    # find the dataset
    ds = pangeo_CMIP_funs.cmip6_via_pangeo(zstore=zstore)

    # if there is a target year, subset the dataset by that year
    if year != None:
        ds = ds.sel(time=ds.time.dt.year.isin([year]))

    return ds


save_path = os.getcwd().replace('\\', '/') + '/'

# plot data
# straight variable at a given time
# plotting_funs.plt_straight_variable(ds, 210)


# Count of days where variable is over a given threshold

# get data from a given year
# year = 2100
year = 2050
# year = 2015


# define threshold
threshold_temp = 30 + constants.convert_kelvin

plotting_funs.plt_count_over_threshold(ds=ds_2015, threshold=threshold_temp, year=year, save_path=save_path)

print('end')
