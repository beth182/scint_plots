# imports
import pandas as pd

from scint_plots.tools.preprocessed_scint_csvs import read_obs_csvs
from scint_plots.tools.preprocessed_UKV_csvs import read_UKV_csvs
from scint_plots.tools import eval_stat_funs

# user choice
scint_path = 15

# read the premade scint data csv files
obs_df = read_obs_csvs.read_all_of_preprocessed_scint_csv(['QH'], average=60)[['QH_' + str(scint_path)]]

# read the premade UKV data csv files

# level 0
df_UKV_0 = read_UKV_csvs.read_all_of_preprocessed_UKV_csv(['BL_H'], model_level=0, grid_priority='primary')[
    ['BL_H_' + str(scint_path)]].rename(columns={'BL_H_' + str(scint_path): 'UKV 0'})

# level 1
df_UKV_1 = read_UKV_csvs.read_all_of_preprocessed_UKV_csv(['BL_H'], model_level=1, grid_priority='primary')[
    ['BL_H_' + str(scint_path)]].rename(columns={'BL_H_' + str(scint_path): 'UKV 1'})

# level -1
df_UKV__1 = read_UKV_csvs.read_all_of_preprocessed_UKV_csv(['BL_H'], model_level=-1, grid_priority='primary')[
    ['BL_H_' + str(scint_path)]].rename(columns={'BL_H_' + str(scint_path): 'UKV -1'})

# level 0 2nd gridbox
df_UKV_0_2 = read_UKV_csvs.read_all_of_preprocessed_UKV_csv(['BL_H'], model_level=0, grid_priority='secondary')[
    ['BL_H_' + str(scint_path)]].rename(columns={'BL_H_' + str(scint_path): 'UKV 0 2'})

# combine UKV df into one
df = pd.concat([obs_df, df_UKV_0, df_UKV_1, df_UKV__1, df_UKV_0_2], axis=1).dropna()

# combine the 1st and 2nd gridbox level 0 together
df['UKV 2 grids'] = (df['UKV 0'] + df['UKV 0 2']) / 2

# perform the hit rate

UKV_column_list = ['UKV 0', 'UKV 1', 'UKV -1', 'UKV 2 grids']

for UKV_col in UKV_column_list:

    print(' ')
    print(UKV_col)
    HR = eval_stat_funs.variable_hitrate(obs=df['QH_' + str(scint_path)],
                                         mod=df[UKV_col])
    print(HR)

print('end')
