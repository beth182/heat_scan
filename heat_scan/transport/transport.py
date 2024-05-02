import os

from heat_scan.tools import constants
from heat_scan.transport import plotting_funs

from heat_scan.tools.pangeo_CMIP import pangeo_CMIP_funs


def run_projections(threshold, experiment_id, variable_id='tasmax', year=None,
                    save_path=os.getcwd().replace('\\', '/') + '/', **kwargs):
    """

    :return:
    """
    # ToDo: docstring here

    ds = pangeo_CMIP_funs.main_find_CMIP(variable_id=variable_id, experiment_id=experiment_id, year=year, **kwargs)

    # plot data
    # straight variable at a given time
    # plotting_funs.plt_straight_variable(ds=ds, year=year, save_path=save_path, time=210)  # 210: summer, 0: winter?

    # Count of days where variable is over a given threshold
    if variable_id == 'tasmax' or variable_id == 'tas':
        threshold += constants.convert_kelvin

    plotting_funs.plt_count_over_threshold(ds=ds, threshold=threshold, year=year, save_path=save_path)


if __name__ == "__main__":
    # get data from a given year
    year = 2015
    # year = 2050
    # year = 2100

    experiment_id = 'ssp245'

    run_projections(threshold=25, experiment_id = experiment_id, year=year)

    print('end')
