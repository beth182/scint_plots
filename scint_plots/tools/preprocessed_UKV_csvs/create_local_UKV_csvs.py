# Beth Saunders 14/02/23
# script to write local csv files with model data

# imports
import os

from model_eval_tools.retrieve_UKV import retrieve_ukv_vars
from scint_flux import look_up

# user choices
scint_path = 15
DOY_list = [2016126, 2016123]

pair_id = look_up.scint_path_numbers[scint_path]
scint_UKV_grid_choices = {'BCT_IMU': 13, 'IMU_BTT': 12, 'BTT_BCT': 12, 'SCT_SWT': 37}

scint_median_zf = {'BCT_IMU': 73.6, 'IMU_BTT': 103.3, 'BTT_BCT': 113.5, 'SCT_SWT': 32.4}

run_details = {'variable': 'BL_H',
               'run_time': '21Z',
               'scint_path': scint_path,
               'grid_number': scint_UKV_grid_choices[pair_id],
               'target_height': scint_median_zf[pair_id]}

for DOY in DOY_list:
    # get model sensible heat
    ukv_data_dict_QH = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details, DOYstart=DOY, DOYstop=DOY)
    UKV_df_QH = retrieve_ukv_vars.UKV_df(ukv_data_dict_QH)

    print('end')

print('end')

save_path = os.getcwd().replace('\\', '/') + '/csv_files/'
