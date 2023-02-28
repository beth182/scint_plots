# Beth Saunders 15/02/23
# Script to produce values for model performance

# imports
import pandas as pd
import numpy as np

from scint_plots.tools.preprocessed_scint_csvs import read_obs_csvs
from scint_plots.tools.preprocessed_UKV_csvs import read_UKV_csvs
from scint_plots.scint_seasonality import seasonality_funs
from scint_plots.tools import eval_stat_funs

# user choices
path_choice = 11
variable = 'QH'
# average = 60
average = 10

if variable == 'QH':
    ukv_variable = 'BL_H'
else:
    ukv_variable = variable

# read the premade scint data csv files
df = read_obs_csvs.read_all_of_preprocessed_scint_csv([variable], average=average)

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

# all seasons together
# HR with variable threshold
HR_all = eval_stat_funs.variable_hitrate(obs=df_all[variable + '_' + str(path_choice)],
                                mod=df_all['UKV_' + variable + '_' + str(path_choice)])

# MAE
MAE_all = df_all.AE.mean()
# MBE
MBE_all = df_all.BE.mean()

# means
mean_obs = df_all[variable + '_' + str(path_choice)].mean()
mean_UKV = df_all['UKV_' + variable + '_' + str(path_choice)].mean()

print(' ')
print('ALL')
print('mean LAS:', mean_obs)
print('mean UKV:', mean_UKV)
print('MBE: ', MBE_all)
print('MAE: ', MAE_all)
print('HR: ', HR_all)

# split by season
season_dict = seasonality_funs.split_df_into_season(df_all)

for season in season_dict:
    print(' ')
    print(season)

    season_df = season_dict[season]

    # HR
    HR_season = eval_stat_funs.variable_hitrate(obs=season_df[variable + '_' + str(path_choice)],
                                       mod=season_df['UKV_' + variable + '_' + str(path_choice)])

    # MAE
    MAE_season = season_df.AE.mean()
    # MBE
    MBE_season = season_df.BE.mean()

    # means
    mean_obs_season = season_df[variable + '_' + str(path_choice)].mean()
    mean_UKV_season = season_df['UKV_' + variable + '_' + str(path_choice)].mean()

    print('mean LAS:', mean_obs_season)
    print('mean UKV:', mean_UKV_season)
    print('MBE: ', MBE_season)
    print('MAE: ', MAE_season)
    print('HR: ', HR_season)

print('end')
