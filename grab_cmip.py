import pandas as pd
import xarray as xr
import gcsfs

# Analysis of Google Cloud CMIP6 data using Pangeo tools.

# instruction: https://medium.com/pangeo/cmip6-in-the-cloud-five-ways-96b177abe396
# variable name table: https://pcmdi.llnl.gov/mips/cmip3/variableList.html#Table_A1f
# Link to pangeo-cmip6.csv: https://cmip6.storage.googleapis.com/pangeo-cmip6.csv

zstore = "gs://cmip6/CMIP6/HighResMIP/CMCC/CMCC-CM2-HR4/highresSST-present/r1i1p1f1/Amon/tas/gn/v20170706/"

fs = gcsfs.GCSFileSystem(token='anon', access='read_only')
mapper = fs.get_mapper(zstore)

# open it using xarray and zarr
ds = xr.open_zarr(mapper, consolidated=True)

# To plot the first time step
# ds.tas.isel(time=0).plot()

print('end')