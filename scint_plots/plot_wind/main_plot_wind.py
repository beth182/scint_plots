import numpy as np

from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up

from model_eval_tools.retrieve_UKV import retrieve_ukv_vars

from scint_plots.plot_wind import plot_wind_funs

scint_path = 12
DOY_list = [2016126, 2016123]
var_list = ['wind_speed_adj', 'wind_direction_corrected', 'z_0']
time_res = '1min_sa10min'

pair_id = look_up.scint_path_numbers[scint_path]

DOY_dict = {}

# read the 10-min SA vars
for DOY in DOY_list:
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res=time_res)

    # get model wind speed and direction
    ukv_data_dict_wind = retrieve_ukv_vars.retrieve_UKV(scint_path, DOY, DOY, variable='wind',
                                                        av_disheight=np.nanmean(df['z_f']) - np.nanmean(df['z_0']))
    UKV_df = retrieve_ukv_vars.UKV_df(ukv_data_dict_wind, wind=True)
    DOY_dict[DOY] = {time_res: df, 'UKV_wind': UKV_df, 'UKV_height': ukv_data_dict_wind['BL_H_z']}

# read the 60-min SA vars
for DOY in DOY_list:
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res='1min')

    DOY_dict[DOY]['1min'] = df

# plot
plot_wind_funs.plot_wind(DOY_dict)
print('end')
