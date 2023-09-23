import os
import numpy as np

from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up
from scint_plots.tools.preprocessed_UKV_csvs import UKV_lookup

from model_eval_tools.retrieve_UKV import retrieve_ukv_vars
from model_eval_tools.sa_analysis_grids import retrieve_weighted_ukv_lc

from scint_plots.built_fraction import built_fraction_funs

scint_path = 12
DOY_list = [2016126, 2016123]
var_list = ['QH', 'kdown']
time_res = '1min_sa10min'

pair_id = look_up.scint_path_numbers[scint_path]

DOY_dict = {}

for DOY in DOY_list:
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res=time_res)

    # combine obs with land cover csv obtained using the SAs
    df = built_fraction_funs.add_lc_to_df(df)

    DOY_dict[DOY] = {'obs': df}

    # get model sensible heat
    run_details_H = {'variable': 'H',
                   'run_time': '21Z',
                   'scint_path': scint_path,
                   'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id][1],  # this is only used if sa_analysis is set to False
                   'target_height': df.z_f.mean()}

    ukv_data_dict_QH = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details_H, DOYstart=DOY, DOYstop=DOY)
    UKV_df_QH = retrieve_ukv_vars.UKV_df(ukv_data_dict_QH)
    DOY_dict[DOY]['UKV_QH'] = UKV_df_QH

    # get model kdown
    run_details_kdown = {'variable': 'kdown',
                   'run_time': '21Z',
                   'scint_path': scint_path,
                   'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id][1],
                   'target_height': np.nan}

    ukv_data_dict_kdown = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details_kdown, DOYstart=DOY, DOYstop=DOY)
    UKV_df_kdown = retrieve_ukv_vars.UKV_df(ukv_data_dict_kdown)
    DOY_dict[DOY]['UKV_kdown'] = UKV_df_kdown

    # get model land cover
    ukv_lc_df = retrieve_weighted_ukv_lc.weight_lc_fractions(ukv_data_dict_QH['model_site_dict'],
                                                             ukv_data_dict_QH['percentage_vals_dict'],
                                                             DOY,
                                                             save_csv=True,
                                                             csv_path=os.getcwd().replace('\\', '/') + '/')

    DOY_dict[DOY]['ukv_lc'] = ukv_lc_df


built_fraction_funs.plot_built_fraction(DOY_dict)

print('end')
