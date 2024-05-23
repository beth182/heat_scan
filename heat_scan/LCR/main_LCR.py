# imports
import os
import pandas as pd

from heat_scan.tools.pangeo_CMIP import pangeo_CMIP_funs
from heat_scan.tools.polygons import polygon_funs


# user inputs
# year = 2015
# year = 2050
# year = 2100

# between 2090 and 2100
# year = list(range(2090, 2101))

# between 2040 and 2050
year = list(range(2040, 2050))

# between 2015 and 2025
# year = list(range(2015, 2026))

# between 2080 and 2100
# year = list(range(2080, 2101))

experiment_id = 'ssp245'
region = 'LCR'

# source_id = 'CSIRO-ARCCSS'
source_id = 'GFDL-ESM4'

# test = True
test = False

########################################################################################################################
country_df = polygon_funs.get_country_df(test=test, region=region)

if source_id == 'GFDL-ESM4':
    pangeo_CMIP_funs.run_projections(threshold=30, variable_id='tasmax', experiment_id=experiment_id, year=year,
                                     region='LCR', source_id=source_id, country_df=country_df, day_threshold_stats=True,
                                     test=test, plot_days_threshold=True)

else:
    assert source_id == 'CSIRO-ARCCSS'
    pangeo_CMIP_funs.run_projections(variable_id='tasmax', threshold=30, experiment_id=experiment_id, year=year,
                                     region=region, institution_id='CSIRO-ARCCSS', source_id='ACCESS-CM2',
                                     member_id='r1i1p1f1', grid_label='gn', country_df=country_df,
                                     day_threshold_stats=True, test=test)
