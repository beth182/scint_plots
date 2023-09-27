# imports
import numpy as np

from scint_flux import look_up
from scint_flux.functions import read_calculated_fluxes
from scint_plots.P1_stats_table import scint_stat_funs
from scint_plots.tools.preprocessed_UKV_csvs import UKV_lookup
from model_eval_tools.retrieve_UKV import retrieve_ukv_vars


# main script for running stat functions of P1: Results table

scint_path = 12
DOY_list = [2016126]

var_list = ['QH', 'kdown', 'z_f']

time_res = '1min_sa10min'
# time_res = '1min'

pair_id = look_up.scint_path_numbers[scint_path]

for DOY in DOY_list:
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res=time_res)

    # stats of observations
    # """
    scint_stat_funs.stats_of_the_obs_fluxes(df)
    print('end')
    # """

    # stats of model
    """
    # retrieve UKV data
    run_details_H = {'variable': 'H',
                   'run_time': '21Z',
                   'scint_path': scint_path,
                   'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id][1],  # this is only used if sa_analysis is set to False
                   'target_height': df.z_f.mean()}
    run_details_kdown = {'variable': 'kdown',
                   'run_time': '21Z',
                   'scint_path': scint_path,
                   'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id][1],  # this is only used if sa_analysis is set to False
                   'target_height': np.nan}

    # get model sensible heat
    ukv_data_dict_QH = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details_H, DOYstart=DOY, DOYstop=DOY)
    UKV_df_QH = retrieve_ukv_vars.UKV_df(ukv_data_dict_QH)
    # get model kdown
    ukv_data_dict_kdown = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details_kdown, DOYstart=DOY, DOYstop=DOY)
    UKV_df_kdown = retrieve_ukv_vars.UKV_df(ukv_data_dict_kdown)

    scint_stat_funs.stats_of_model(df, UKV_df_QH, UKV_df_kdown)
    print('end')

    """
