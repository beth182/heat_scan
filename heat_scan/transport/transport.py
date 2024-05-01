import os

from heat_scan.tools.pangeo_CMIP import pangeo_CMIP_funs
from heat_scan.tools import constants
from heat_scan.transport import plotting_funs





if __name__ == "__main__":
    save_path = os.getcwd().replace('\\', '/') + '/'

    # get data from a given year
    # year = 2100
    year = 2050
    # year = 2015

    # plot data
    # straight variable at a given time
    # plotting_funs.plt_straight_variable(ds=ds, year=year, save_path=save_path, time=210)  # 210: summer?

    # Count of days where variable is over a given threshold
    # define threshold
    threshold_temp = 30 + constants.convert_kelvin
    plotting_funs.plt_count_over_threshold(ds=ds, threshold=threshold_temp, year=year, save_path=save_path)

    print('end')
