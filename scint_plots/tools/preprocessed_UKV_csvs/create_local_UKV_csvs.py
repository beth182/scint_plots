# Beth Saunders 14/02/23
# script to write local csv files with model data

# imports
import os
import pandas as pd
import datetime as dt
import numpy as np

from scint_plots.tools.preprocessed_UKV_csvs import UKV_lookup
from model_eval_tools.retrieve_UKV import retrieve_ukv_vars
from scint_flux import look_up

# user choices
scint_path = 15

# read in all DOYs for the selected path
# read in csv with days
DOY_df = pd.read_csv('C:/Users/beths/OneDrive - University of Reading/Paper 2/all_days.csv')
# take only days of the target path
scint_path_string = 'P' + str(scint_path)
df_subset = DOY_df.iloc[np.where(DOY_df[scint_path_string] == 1)[0]]
df_subset['DOY_string'] = df_subset.year.astype(str) + df_subset.DOY.astype(str)
df_subset['DOY_string'] = df_subset['DOY_string'].astype(int)
DOY_list = df_subset.DOY_string.to_list()

# FOR TESTING
# DOY_list = DOY_list[:2]

pair_id = look_up.scint_path_numbers[scint_path]

DOY_df_list = []
model_level_heights = []

for DOY in DOY_list:

    # get model sensible heat - BL_H
    run_details_BL_H = {'variable': 'BL_H',
                        'run_time': '21Z',
                        'scint_path': scint_path,
                        'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id],
                        'target_height': UKV_lookup.scint_median_zf[pair_id]}

    ukv_data_dict_QH = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details_BL_H, DOYstart=DOY, DOYstop=DOY)
    UKV_df_QH = retrieve_ukv_vars.UKV_df(ukv_data_dict_QH)

    model_level_height = round(ukv_data_dict_QH['BL_H_z'])
    model_level_heights.append(model_level_height)
    ####################################################################################################################

    # get model wind
    run_details_wind = {'variable': 'wind',
                        'run_time': '21Z',
                        'scint_path': scint_path,
                        'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id],
                        'target_height': UKV_lookup.scint_median_zf[pair_id]}

    # get model wind speed and direction
    ukv_data_dict_wind = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details_wind, DOYstart=DOY, DOYstop=DOY)

    UKV_df_wind = retrieve_ukv_vars.UKV_df(ukv_data_dict_wind, wind=True)
    ####################################################################################################################

    # get model kdown
    run_details_kdown = {'variable': 'kdown',
                         'run_time': '21Z',
                         'scint_path': scint_path,
                         'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id],
                         'target_height': 0  # surface stash code
                         }

    ukv_data_dict_kdown = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details_kdown, DOYstart=DOY, DOYstop=DOY,
                                                         sa_analysis=False)

    UKV_df_kdown = retrieve_ukv_vars.UKV_df(ukv_data_dict_kdown)

    # push back kdown (15 min average time starting) by 15 mins to match QH time (instantaneous on the hour)
    UKV_df_kdown.index = UKV_df_kdown.index - dt.timedelta(minutes=15)

    # rename column to kdown (is orignially grid)
    UKV_df_kdown = UKV_df_kdown.rename(columns={UKV_lookup.scint_UKV_grid_choices[pair_id]: 'kdown'})
    ####################################################################################################################

    # combine all variables into one df
    DOY_df = pd.concat([UKV_df_QH, UKV_df_kdown, UKV_df_wind], axis=1)
    DOY_df_list.append(DOY_df)
    print(DOY)


assert model_level_heights.count(model_level_heights[0]) == len(model_level_heights)

df_all = pd.concat(DOY_df_list)
save_path = os.getcwd().replace('\\', '/') + '/UKV_csv_files/'
df_all.to_csv(save_path + 'grid_' + str(UKV_lookup.scint_UKV_grid_choices[pair_id]) + '_height_' + str(model_level_heights[0]) + '_' + pair_id + '_vals.csv')
print('end')
