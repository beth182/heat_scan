# imports
import xarray as xr
import gcsfs


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