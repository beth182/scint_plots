from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up

from model_eval_tools.retrieve_UKV import retrieve_ukv_vars

from scint_plots.tools.preprocessed_UKV_csvs import UKV_lookup
from scint_plots.detailed_time_series import detailed_time_series_funs

import numpy as np

scint_path = 12
DOY_list = [2016123, 2016126]
var_list = ['kdown', 'z_0']
time_res = '1min_sa10min'

pair_id = look_up.scint_path_numbers[scint_path]

DOY_dict = {}

for DOY in DOY_list:
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res=time_res)

    DOY_dict[DOY] = {time_res: df}

    # get model kdown
    # retrieve UKV data

    run_details = {'variable': 'kdown',
                   'run_time': '21Z',
                   'scint_path': scint_path,
                   'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id][1],
                   'target_height': np.nan}

    ukv_data_dict_kdown = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details, DOYstart=DOY, DOYstop=DOY)
    UKV_df_kdown = retrieve_ukv_vars.UKV_df(ukv_data_dict_kdown)

    DOY_dict[DOY] = {'obs': df, 'UKV_kdown': UKV_df_kdown}

    detailed_time_series_funs.detailed_time_series(obs_df=df,
                                                   ukv_df=UKV_df_kdown,
                                                   model_site_dict=ukv_data_dict_kdown['model_site_dict'],
                                                   variable='kdown',
                                                   model_site_dict_all=ukv_data_dict_kdown['all_grids_kdown_dict'][
                                                       'model_site_dict_all'])

print('end')
