# Beth Saunders 15/02/23
# Script to produce values for model performance

# imports
import pandas as pd
import numpy as np

from scint_plots.tools.preprocessed_scint_csvs import read_obs_csvs
from scint_plots.tools.preprocessed_UKV_csvs import read_UKV_csvs
from scint_plots.scint_seasonality import seasonality_funs

# user choices
path_choice = 15
variable = 'QH'

if variable == 'QH':
    ukv_variable = 'BL_H'
else:
    ukv_variable = variable

# read the premade scint data csv files
df = read_obs_csvs.read_all_of_preprocessed_scint_csv([variable])

# read the premade UKV data csv files
df_UKV = read_UKV_csvs.read_all_of_preprocessed_UKV_csv([ukv_variable])

# drop any path other than the one chosen
for col in df.columns:
    if path_choice == int(col.split('_')[-1]):
        pass
    else:
        df = df.drop(columns=[col])

for col in df_UKV.columns:
    if path_choice == int(col.split('_')[-1]):
        pass
    else:
        df_UKV = df_UKV.drop(columns=[col])

# drop nas
df = df.dropna()
df_UKV = df_UKV.dropna()

# rename cols in UKV
df_UKV = df_UKV.rename(columns={ukv_variable + '_' + str(path_choice): 'UKV_' + variable + '_' + str(path_choice)})

# combine dfs
df_all = pd.concat([df, df_UKV], axis=1).dropna()

# take difference between model and obs
df_all['BE'] = df_all[variable + '_' + str(path_choice)] - df_all['UKV_' + variable + '_' + str(path_choice)]
df_all['AE'] = np.abs(df_all[variable + '_' + str(path_choice)] - df_all['UKV_' + variable + '_' + str(path_choice)])

# HR



# split by season
season_dict = seasonality_funs.split_df_into_season(df_all)

for season in season_dict:
    print(season)

    season_df = season_dict[season]



    print('end')

print('end')
