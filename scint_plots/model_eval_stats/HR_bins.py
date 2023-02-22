# Beth Saunders 21/02/23
# HR stats for multiple values in a bin - lenient model level / path choices

# imports
import pandas as pd

from scint_plots.tools.preprocessed_scint_csvs import read_obs_csvs
from scint_plots.tools.preprocessed_UKV_csvs import read_UKV_csvs
from scint_plots.tools import eval_stat_funs
from scint_plots.tools.preprocessed_UKV_csvs import UKV_lookup
from scint_plots.scint_seasonality import seasonality_funs

# user choices
variable = 'QH'
average = 10

if variable == 'QH':
    ukv_variable = 'BL_H'
else:
    ukv_variable = variable

# read the premade scint data csv files: for 3 paths
df = read_obs_csvs.read_all_of_preprocessed_scint_csv([variable], average=average)

# drop unneeded column of SCT_SWT
df = df.drop(columns=[variable + '_15'])

# drop times where all 3 paths are not avail
df = df.dropna()

# read UKV for multiple levels
model_level_list = [-1, 0, 1]

UKV_df_list = []

for model_level in model_level_list:
    # read the premade UKV data csv files: for multiple paths, and for multiple levels
    df_UKV = read_UKV_csvs.read_all_of_preprocessed_UKV_csv([ukv_variable], model_level=model_level)

    # drop unneeded column of SCT_SWT
    df_UKV = df_UKV.drop(columns=[ukv_variable + '_15'])

    # confirm that the path 11 and path 13 columns are identical
    assert (df_UKV.BL_H_11 - df_UKV.BL_H_13).sum() == 0
    df_UKV = df_UKV.drop(columns='BL_H_13')

    # get rid of any times where one path is missing
    df_UKV = df_UKV.dropna()

    # get heights
    height_11 = UKV_lookup.model_level_heights['BTT_BCT'][model_level]
    height_12 = UKV_lookup.model_level_heights['BCT_IMU'][model_level]

    # add heights to columns
    for col in df_UKV.columns:

        if int(col.split('_')[-1]) == 11:
            new_name = col + '_' + str(height_11)
        else:
            assert int(col.split('_')[-1]) == 12
            new_name = col + '_' + str(height_12)

        df_UKV = df_UKV.rename(columns={col: new_name})

    UKV_df_list.append(df_UKV)

df_all_UKV = pd.concat(UKV_df_list, axis=1)

# combine dfs
df_all = pd.concat([df, df_all_UKV], axis=1).dropna()

print(' ')
print('HR: ALL seasons')
HR = eval_stat_funs.hitrate_bins(df_all)
print(HR)

# split by season
season_dict = seasonality_funs.split_df_into_season(df_all)

for season in season_dict.keys():
    print(' ')
    print(season)
    df_season = season_dict[season]
    HR_season = eval_stat_funs.hitrate_bins(df_season)
    print(HR_season)


print('end')
