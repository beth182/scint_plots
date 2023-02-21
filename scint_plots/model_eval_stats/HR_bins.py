# Beth Saunders 21/02/23
# HR stats for multiple values in a bin - lenient model level / path choices

# imports
import pandas as pd
import numpy as np

from scint_plots.tools.preprocessed_scint_csvs import read_obs_csvs
from scint_plots.tools.preprocessed_UKV_csvs import read_UKV_csvs
from scint_plots.tools import eval_stat_funs
from scint_plots.tools.preprocessed_UKV_csvs import UKV_lookup

# user choices
variable = 'QH'
average = 60

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





# perform hit rate function

df = df_all.copy()
# identify obs columns
obs_cols = []
ukv_cols = []
for col in df:
    if col.startswith('QH'):
        obs_cols.append(col)
    else:
        ukv_cols.append(col)

df['max'] = df[obs_cols].max(axis=1)
df['min'] = df[obs_cols].min(axis=1)

# take 10 percent
df['max_threshold'] = df['max'] + (df['max'] / 100) * 10
df['min_threshold'] = df['min'] - (df['min'] / 100) * 10

model_hits_cols = []
for col in ukv_cols:

    # hits name
    hit_col_name = col + '_hits'
    model_hits_cols.append(hit_col_name)

    # set up dataframe with column of zeros
    df[hit_col_name] = np.zeros(len(df))
    df[hit_col_name][(df[col] >= df['min_threshold']) & (df[col] <= df['max_threshold'])] = 1

# sum the hits
df[model_hits_cols].mean().mean() * 100

print('end')
