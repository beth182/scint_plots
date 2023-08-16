import numpy as np

from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up

from scint_plots.stability_and_SA import stability_and_SA_funs
from scint_plots.tools.preprocessed_UKV_csvs import UKV_lookup

from model_eval_tools.retrieve_UKV import retrieve_ukv_vars

scint_path = 12
DOY_list = [2016126, 2016123]
var_list = ['z_0', 'z_d', 'z_f', 'sa_area_km2', 'ustar', 'stab_param', 'wind_speed_adj', 'wind_direction_corrected']
time_res = '1min_sa10min'

pair_id = look_up.scint_path_numbers[scint_path]

DOY_dict = {}

# read the 60-min SA vars
for DOY in DOY_list:
    DOY_dict[DOY] = {}
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res='1min')
    DOY_dict[DOY]['1min'] = df

    # get model wind
    run_details_wind = {'variable': 'wind',
                        'run_time': '21Z',
                        'scint_path': scint_path,
                        'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id][1],
                        'target_height': np.nanmean(df['z_f']) - np.nanmean(df['z_0'])}

    # get model wind speed and direction
    ukv_data_dict_wind = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details_wind, DOYstart=DOY, DOYstop=DOY)

    UKV_df = retrieve_ukv_vars.UKV_df(ukv_data_dict_wind, wind=True)

    DOY_dict[DOY]['UKV'] = {'UKV_wind': UKV_df, 'UKV_height': ukv_data_dict_wind['BL_H_z']}

# read the 10-min SA vars
for DOY in DOY_list:
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res=time_res)

    DOY_dict[DOY][time_res] = df

# plot
stability_and_SA_funs.stability_and_sa(DOY_dict)
print('end')
