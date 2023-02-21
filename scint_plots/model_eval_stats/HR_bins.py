# Beth Saunders 21/02/23
# HR stats for multiple values in a bin - lenient model level / path choices

# imports
import pandas as pd
import numpy as np

from scint_plots.tools.preprocessed_scint_csvs import read_obs_csvs
from scint_plots.tools.preprocessed_UKV_csvs import read_UKV_csvs
from scint_plots.tools import eval_stat_funs

# user choices
variable = 'QH'
average = 60

if variable == 'QH':
    ukv_variable = 'BL_H'
else:
    ukv_variable = variable

# read the premade scint data csv files: for 3 paths
df = read_obs_csvs.read_all_of_preprocessed_scint_csv([variable], average=average)

# read the premade UKV data csv files: for multiple paths, and for multiple levels
df_UKV_0 = read_UKV_csvs.read_all_of_preprocessed_UKV_csv([ukv_variable], model_level=0)
df_UKV__1 = read_UKV_csvs.read_all_of_preprocessed_UKV_csv([ukv_variable], model_level=-1)
df_UKV_1 = read_UKV_csvs.read_all_of_preprocessed_UKV_csv([ukv_variable], model_level=1)


# drop unneeded column of SCT_SWT
df = df.drop(columns=[variable + '_15'])
df_UKV = df_UKV.drop(columns=[ukv_variable + '_15'])


# drop times where all 3 paths are not avail
df = df.dropna()
df_UKV = df_UKV.dropna()

# combine dfs
df_all = pd.concat([df, df_UKV], axis=1).dropna()

print('end')
