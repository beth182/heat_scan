from heat_scan.LCR import LCR_functions


import pandas as pd

# for Google Cloud:
df = pd.read_csv("https://cmip6.storage.googleapis.com/pangeo-cmip6.csv")



# df_subset = df.query("institution_id=='MOHC' & activity_id=='ScenarioMIP' & table_id=='3hr' & variable_id=='tas'")

df_subset = df.query("activity_id=='ScenarioMIP' & table_id=='day' & variable_id=='tasmax'")

print('end')