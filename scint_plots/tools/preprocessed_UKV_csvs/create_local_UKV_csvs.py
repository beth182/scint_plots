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

########################################################################################################################

# user choices
scint_path = 11

# target model levels.
# 0 = closest level to obs median zf
# 1 is one above
# -1 is one bellow
target_level = -1

# target grid - primary or secondary grid for this site?
target_grid = 'primary'
# target_grid = 'secondary'


########################################################################################################################

# read in all DOYs for the selected path
# read in csv with days
DOY_df = pd.read_csv('C:/Users/beths/OneDrive - University of Reading/Paper 2/all_days.csv')
# take only days of the target path
scint_path_string = 'P' + str(scint_path)
df_subset = DOY_df.iloc[np.where(DOY_df[scint_path_string] == 1)[0]]
df_subset['DOY_string'] = df_subset.year.astype(str) + df_subset.DOY.astype(str)
df_subset['DOY_string'] = df_subset['DOY_string'].astype(int)
DOY_list = df_subset.DOY_string.to_list()

# for testing
# DOY_list = DOY_list[:2]

pair_id = look_up.scint_path_numbers[scint_path]

# set the grid index
if target_grid == 'primary':
    grid_ind = 1
else:
    assert target_grid == 'secondary'
    grid_ind = 2


# set the target height
if target_level == 0:  # exact model level
    target_height = UKV_lookup.scint_median_zf[pair_id]

elif target_level == 1:  # going up a model level
    if pair_id == 'SCT_SWT' or pair_id == 'BCT_IMU':  # going from level 3 to level 4
        target_height = UKV_lookup.scint_median_zf[pair_id] + 26.666668

    else:  # going from level 4 to 5
        target_height = UKV_lookup.scint_median_zf[pair_id] + 33.333321

elif target_level == -1:  # going down a model level
    if pair_id == 'SCT_SWT':  # going from level 3 to 2
        target_height = UKV_lookup.scint_median_zf[pair_id] - 20.000002

    elif pair_id == 'BCT_IMU':  # going from level 3 to 2 - but for some reason I need to take a bit more for just this case
        target_height = UKV_lookup.scint_median_zf[pair_id] - 20.000002 - 5

    else:  # going from level 4 to 3
        target_height = UKV_lookup.scint_median_zf[pair_id] - 26.666668
else:
    raise ValueError('Target level has to be -1, 0 or 1.')

DOY_df_list = []
model_level_heights = []

for DOY in DOY_list:
    # get model sensible heat - BL_H
    run_details_BL_H = {'variable': 'BL_H',
                        'run_time': '21Z',
                        'scint_path': scint_path,
                        'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id][grid_ind],
                        'target_height': target_height}

    ukv_data_dict_QH = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details_BL_H, DOYstart=DOY, DOYstop=DOY)
    UKV_df_QH = retrieve_ukv_vars.UKV_df(ukv_data_dict_QH)

    model_level_height = round(ukv_data_dict_QH['BL_H_z'])
    model_level_heights.append(model_level_height)
    ####################################################################################################################

    # get model wind
    run_details_wind = {'variable': 'wind',
                        'run_time': '21Z',
                        'scint_path': scint_path,
                        'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id][grid_ind],
                        'target_height': target_height}

    # get model wind speed and direction
    ukv_data_dict_wind = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details_wind, DOYstart=DOY, DOYstop=DOY)

    UKV_df_wind = retrieve_ukv_vars.UKV_df(ukv_data_dict_wind, wind=True)
    ####################################################################################################################

    # get model kdown
    run_details_kdown = {'variable': 'kdown',
                         'run_time': '21Z',
                         'scint_path': scint_path,
                         'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id][grid_ind],
                         'target_height': 0  # surface stash code
                         }

    ukv_data_dict_kdown = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details_kdown, DOYstart=DOY, DOYstop=DOY,
                                                         sa_analysis=False)

    UKV_df_kdown = retrieve_ukv_vars.UKV_df(ukv_data_dict_kdown)

    # push back kdown (15 min average time starting) by 15 mins to match QH time (instantaneous on the hour)
    UKV_df_kdown.index = UKV_df_kdown.index - dt.timedelta(minutes=15)

    # rename column to kdown (is orignially grid)
    UKV_df_kdown = UKV_df_kdown.rename(columns={UKV_lookup.scint_UKV_grid_choices[pair_id][grid_ind]: 'kdown'})
    ####################################################################################################################

    # combine all variables into one df
    DOY_df = pd.concat([UKV_df_QH, UKV_df_kdown, UKV_df_wind], axis=1)
    DOY_df_list.append(DOY_df)
    print(DOY)

assert model_level_heights.count(model_level_heights[0]) == len(model_level_heights)

df_all = pd.concat(DOY_df_list)
save_path = os.getcwd().replace('\\', '/') + '/UKV_csv_files/'
df_all.to_csv(save_path + 'grid_' + str(UKV_lookup.scint_UKV_grid_choices[pair_id][grid_ind]) + '_height_' + str(
    model_level_heights[0]) + '_' + pair_id + '_vals.csv')
print('end')
