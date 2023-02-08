# imports
import pandas as pd
import os
import numpy as np

from scint_flux import look_up

from scint_plots.built_fraction_multiple import lc_fraction_funs
from scint_plots.built_fraction_multiple import plotting_funs

# user choice
path_list = [15,11]

save_path = os.getcwd().replace('\\', '/') + '/'

path_dict = {}
for scint_path in path_list:

    pair_id = look_up.scint_path_numbers[scint_path]


    # read in all files
    # read in csv with days
    # DOY_df = pd.read_csv('C:/Users/beths/OneDrive - University of Reading/Paper 2/days_to_be_read_in.csv')
    DOY_df = pd.read_csv('C:/Users/beths/OneDrive - University of Reading/Paper 2/all_days.csv')
    # take only days of the target path
    scint_path_string = 'P' + str(scint_path)
    df_subset = DOY_df.iloc[np.where(DOY_df[scint_path_string] == 1)[0]]
    df_subset['DOY_string'] = df_subset.year.astype(str) + df_subset.DOY.astype(str)
    df_subset['DOY_string'] = df_subset['DOY_string'].astype(int)
    DOY_list = df_subset.DOY_string.to_list()


    lc_df = lc_fraction_funs.read_preprocessed_lc_csv(scint_path=scint_path, DOY_list=DOY_list, save_path=save_path)
    scint_df = lc_fraction_funs.read_preprocessed_scint_csv(scint_path=scint_path, DOY_list=DOY_list, save_path=save_path)

    # combine lc fraction csv's and pre-read hourly data csvs
    df = pd.concat([scint_df, lc_df], axis=1)

    # plotting_funs.plot_built_fraction_3(df, pair_id, save_path)

    path_dict[pair_id] = df

plotting_funs.plot_built_fraction_4(path_dict, save_path)


print('end')