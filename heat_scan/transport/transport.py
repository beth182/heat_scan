import os

from heat_scan.tools import constants
from heat_scan.transport import plotting_funs

from heat_scan.tools.pangeo_CMIP import pangeo_CMIP_funs


def run_projections(threshold, year=None, region=None,
                    save_path=os.getcwd().replace('\\', '/') + '/', **kwargs):
    """

    :return:
    """
    # ToDo: docstring here

    ds = pangeo_CMIP_funs.main_find_CMIP(year=year, **kwargs)

    # plot data
    # straight variable at a given time
    # plotting_funs.plt_straight_variable(ds=ds, year=year, save_path=save_path, time=210)  # 210: summer, 0: winter?

    # Count of days where variable is over a given threshold
    assert 'variable_id' in kwargs.keys()
    variable_id = kwargs['variable_id']
    if variable_id == 'tasmax' or variable_id == 'tas':
        threshold += constants.convert_kelvin

    plotting_funs.plt_count_over_threshold(ds=ds, threshold=threshold, year=year, save_path=save_path, region=region, **kwargs)


if __name__ == "__main__":
    # get data from a given year
    # year = 2015
    year = 2050
    # year = 2100

    experiment_id = 'ssp245'

    # defult
    run_projections(threshold=30, variable_id = 'tasmax', experiment_id = experiment_id, year=year, region='LCR')

    # run_projections(variable_id = 'tasmax', threshold=30, experiment_id=experiment_id, year=year, region='LCR', institution_id='CSIRO-ARCCSS', source_id='ACCESS-CM2', member_id='r1i1p1f1', grid_label='gn')



    print('end')
