# imports
import xarray as xr
import gcsfs
import os
import pandas as pd


def cmip6_via_pangeo(zstore, plot=False):
    """
    Alternative way (to CCKP) of getting CMIP6 data: Suggested by Matthias.
    Analysis of Google Cloud CMIP6 data using Pangeo tools.
    instruction: https://medium.com/pangeo/cmip6-in-the-cloud-five-ways-96b177abe396
    variable name table: https://pcmdi.llnl.gov/mips/cmip3/variableList.html#Table_A1f
    Link to pangeo-cmip6.csv: https://cmip6.storage.googleapis.com/pangeo-cmip6.csv

    :return:
    """

    # zstore info:
    # ToDo: put in docstring
    # link provided by Matthias
    # last number, e.g. "20170706" is variable code, listed in the included pangeo-cmip6.csv file, and identified
    # using the table from the link:
    # https://pcmdi.llnl.gov/mips/cmip3/variableList.html#Table_A1f

    fs = gcsfs.GCSFileSystem(token='anon', access='read_only')
    mapper = fs.get_mapper(zstore)

    # open it using xarray and zarr
    ds = xr.open_zarr(mapper, consolidated=True)

    # change lon from degrees east to between -180 to 180
    ds.coords['lon'] = (ds.coords['lon'] + 180) % 360 - 180
    ds = ds.sortby(ds.lon)

    if plot:
        # To plot the first time step
        ds.tas.isel(time=0).plot()

    return ds


def search_pangeo_lookup(variable_id, experiment_id, activity_id='ScenarioMIP', institution_id='NOAA-GFDL',
                         source_id='GFDL-ESM4', member_id='r1i1p1f1', table_id='day', grid_label='gr1'):
    """

    :param variable_id:
    :param experiment_id: e.g. SSP for ScenarioMIP
    :param activity_id:
    :param institution_id:
    :param source_id:
    :param member_id:
    :param table_id:
    :param grid_label:
    :return:
    """

    # note: previously have used:
    # 'gs://cmip6/CMIP6/ScenarioMIP/NOAA-GFDL/GFDL-ESM4/ssp245/r1i1p1f1/day/tasmax/gr1/v20180701/'
    # 'gs://cmip6/CMIP6/ScenarioMIP/NOAA-GFDL/GFDL-ESM4/ssp585/r1i1p1f1/day/tasmax/gr1/v20180701/'
    # 'gs://cmip6/CMIP6/ScenarioMIP/CCCma/CanESM5/ssp245/r1i1p2f1/day/tasmax/gn/v20190429/'
    # 'gs://cmip6/CMIP6/ScenarioMIP/BCC/BCC-CSM2-MR/ssp245/r1i1p1f1/day/tasmax/gn/v20190318/'

    # ToDo: docstring here

    csv_file_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/pangeo-cmip6.csv'

    df_all = pd.read_csv(csv_file_path)

    df = df_all.loc[(df_all['variable_id'] == variable_id) &
                    (df_all['experiment_id'] == experiment_id) &
                    (df_all['activity_id'] == activity_id) &
                    (df_all['institution_id'] == institution_id) &
                    (df_all['source_id'] == source_id) &
                    (df_all['member_id'] == member_id) &
                    (df_all['table_id'] == table_id) &
                    (df_all['grid_label'] == grid_label)
                    ]

    # if df is bigger than one entry, flag
    if len(df) > 1:
        print('end')

    zstore = df.zstore.values[0]
    return zstore


def main_find_CMIP(zstore=None, year=None, **kwargs):
    """

    :param variable_id:
    :param experiment_id:
    :param year:
    :return:
    """
    # ToDo: docstring here

    if zstore == None:
        assert 'variable_id' in kwargs.keys()
        assert 'experiment_id' in kwargs.keys()

        variable_id = kwargs['variable_id']
        experiment_id = kwargs['experiment_id']

        zstore = search_pangeo_lookup(variable_id=variable_id, experiment_id=experiment_id)

    # find the dataset
    ds = cmip6_via_pangeo(zstore=zstore)

    # if there is a target year, subset the dataset by that year
    if year != None:
        ds = ds.sel(time=ds.time.dt.year.isin([year]))

    return ds
