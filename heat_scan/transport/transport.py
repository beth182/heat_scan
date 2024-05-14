from heat_scan.tools.pangeo_CMIP import pangeo_CMIP_funs

if __name__ == "__main__":
    # get data from a given year
    # year = 2015
    year = 2050
    # year = 2100

    experiment_id = 'ssp245'

    # defult
    pangeo_CMIP_funs.run_projections(threshold=30, variable_id='tasmax', experiment_id=experiment_id, year=year,
                                     region='LCR', plot_days_threshold=True)

    # pangeo_CMIP_funs.run_projections(variable_id = 'tasmax', threshold=30, experiment_id=experiment_id, year=year, region='LCR', institution_id='CSIRO-ARCCSS', source_id='ACCESS-CM2', member_id='r1i1p1f1', grid_label='gn', plot_days_threshold=True)

    print('end')
