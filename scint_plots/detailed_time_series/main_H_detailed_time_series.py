import numpy as np

from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up

from scint_plots.tools import combine_obs_averages

from model_eval_tools.retrieve_UKV import retrieve_ukv_vars

from scint_plots.tools.preprocessed_UKV_csvs import UKV_lookup
from scint_plots.detailed_time_series import detailed_time_series_funs

scint_path = 12
DOY_list = [2016126, 2016123]
var_list = ['QH', 'z_f']
time_res = '1min_sa10min'

pair_id = look_up.scint_path_numbers[scint_path]

DOY_dict = {}

for DOY in DOY_list:
    # read the observations
    # 1 min
    df_1 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                               pair_id=pair_id,
                                               var_list=var_list,
                                               time_res=time_res + '_PERIOD_VAR_' + str(1))

    # 5 min
    df_5 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                               pair_id=pair_id,
                                               var_list=var_list,
                                               time_res=time_res + '_PERIOD_VAR_' + str(5))

    # 10 min
    df_10 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                                pair_id=pair_id,
                                                var_list=var_list,
                                                time_res=time_res + '_PERIOD_VAR_' + str(10))

    # 60 min
    df_60 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                                pair_id=pair_id,
                                                var_list=var_list,
                                                time_res='1min' + '_PERIOD_VAR_' + str(60))

    df = combine_obs_averages.combine([df_1, df_5, df_10, df_60], on_hour=False)



    DOY_dict[DOY] = {time_res: df}

    # get model sensible heat
    # retrieve UKV data

    run_details = {'variable': 'H',
                   'run_time': '21Z',
                   'scint_path': scint_path,
                   'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id][1],  # this is only used if sa_analysis is set to False
                   'target_height': df_1.z_f.mean()}

    ukv_data_dict_QH = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details, DOYstart=DOY, DOYstop=DOY)
    UKV_df_QH = retrieve_ukv_vars.UKV_df(ukv_data_dict_QH)
    DOY_dict[DOY] = {'obs': df, 'UKV_QH': UKV_df_QH}

    detailed_time_series_funs.detailed_time_series(obs_df=df,
                                                   ukv_df=UKV_df_QH,
                                                   model_site_dict=ukv_data_dict_QH['model_site_dict'],
                                                   BL_H_z=ukv_data_dict_QH['BL_H_z'],
                                                   variable='H',
                                                   number_grids_axes=False
                                                   )

print('end')
