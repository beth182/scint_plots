import numpy as np

from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up

from model_eval_tools.retrieve_UKV import retrieve_ukv_vars

from scint_plots.tools.preprocessed_UKV_csvs import UKV_lookup
from scint_plots.plot_wind import plot_wind_funs

scint_path = 12
DOY_list = [2016126, 2016123]
var_list = ['wind_speed_adj', 'wind_direction_corrected', 'z_0']
time_res = '1min_sa10min'

pair_id = look_up.scint_path_numbers[scint_path]

DOY_dict = {}

# This plot has since been removed from SM:
# the figure caption used to read:
"""
Figure SM.2: a cloudy (a,c) and clear (b,d) day’s wind speed (a,b) and direction (c,d). Observations (markers), 
with symbol/ colour denoting averaging period. Hourly averages calculated using 60-min SAs. All other averages use 
the 10-min SAs. UKV model prognostic wind direction and wind speed (blue line, hourly samples) at the model level 
closest to the observation height (zf – z0).
"""

# read the 10-min SA vars
for DOY in DOY_list:
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res=time_res)



    # get model wind
    run_details_wind = {'variable': 'wind',
                        'run_time': '21Z',
                        'scint_path': scint_path,
                        'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id][1],
                        'target_height': np.nanmean(df['z_f']) - np.nanmean(df['z_0'])}

    # get model wind speed and direction
    ukv_data_dict_wind = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details_wind, DOYstart=DOY, DOYstop=DOY)

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
