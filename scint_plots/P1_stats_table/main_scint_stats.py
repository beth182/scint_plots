# imports
import numpy as np

from scint_flux import look_up
from scint_flux.functions import read_calculated_fluxes
from scint_plots.P1_stats_table import scint_stat_funs
from scint_plots.tools.preprocessed_UKV_csvs import UKV_lookup
from model_eval_tools.retrieve_UKV import retrieve_ukv_vars

# main script for running stat functions of P1: Results table

scint_path = 12
DOY_list = [2016123, 2016126]

var_list = ['QH', 'kdown', 'z_f']

time_res = '1min_sa10min'
# time_res = '1min'

pair_id = look_up.scint_path_numbers[scint_path]

DOY_dict = {}

for DOY in DOY_list:
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res=time_res)

    DOY_dict[DOY] = {'obs': df}

    # stats of observations
    """
    scint_stat_funs.stats_of_the_obs_fluxes(df)
    print('end')
    """

    # stats of model
    # """
    # retrieve UKV data
    run_details_H = {'variable': 'H',
                     'run_time': '21Z',
                     'scint_path': scint_path,
                     'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id][1],
                     # this is only used if sa_analysis is set to False
                     'target_height': df.z_f.mean()}
    run_details_kdown = {'variable': 'kdown',
                         'run_time': '21Z',
                         'scint_path': scint_path,
                         'grid_number': UKV_lookup.scint_UKV_grid_choices[pair_id][1],
                         # this is only used if sa_analysis is set to False
                         'target_height': np.nan}

    # get model sensible heat
    ukv_data_dict_QH = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details_H, DOYstart=DOY, DOYstop=DOY)
    UKV_df_QH = retrieve_ukv_vars.UKV_df(ukv_data_dict_QH)
    # get model kdown
    ukv_data_dict_kdown = retrieve_ukv_vars.retrieve_UKV(run_choices=run_details_kdown, DOYstart=DOY, DOYstop=DOY)
    UKV_df_kdown = retrieve_ukv_vars.UKV_df(ukv_data_dict_kdown)

    scint_stat_funs.stats_of_model(df, UKV_df_QH, UKV_df_kdown)

    DOY_dict[DOY]['UKV_QH'] = UKV_df_QH

    # print('end')
    # """

print('end')




# Looking at % difference in model fluxes
# """

# constrain times to be just within analysis period
DOY_dict[2016126]['UKV_QH'] = DOY_dict[2016126]['UKV_QH'].dropna()
DOY_dict[2016123]['UKV_QH'] = DOY_dict[2016123]['UKV_QH'].dropna()

# Looking at % difference in fluxes between centre and weighted boxes at surface
DOY_dict[2016126]['UKV_QH']['surf_centre_diff'] = ((DOY_dict[2016126]['UKV_QH'][13] - DOY_dict[2016126]['UKV_QH'][
    'WAverage']) / DOY_dict[2016126]['UKV_QH'][13]) * 100
DOY_dict[2016123]['UKV_QH']['surf_centre_diff'] = ((DOY_dict[2016123]['UKV_QH'][13] - DOY_dict[2016123]['UKV_QH'][
    'WAverage']) / DOY_dict[2016123]['UKV_QH'][13]) * 100
# mean percentage difference
print(' ')
print('MEAN % DIFFERENCE')
print(126, ': ', DOY_dict[2016126]['UKV_QH']['surf_centre_diff'].mean())
print(123, ': ', DOY_dict[2016123]['UKV_QH']['surf_centre_diff'].mean())
# max
print(' ')
print('MAX % DIFFERENCE')
print(126, ': ', DOY_dict[2016126]['UKV_QH']['surf_centre_diff'].iloc[
    np.where(DOY_dict[2016126]['UKV_QH']['surf_centre_diff'] == DOY_dict[2016126]['UKV_QH']['surf_centre_diff'].max())[
        0]])
print(123, ': ', DOY_dict[2016123]['UKV_QH']['surf_centre_diff'].iloc[
    np.where(DOY_dict[2016123]['UKV_QH']['surf_centre_diff'] == DOY_dict[2016123]['UKV_QH']['surf_centre_diff'].max())[
        0]])
# min
print(' ')
print('MIN % DIFFERENCE')
print(126, ': ', DOY_dict[2016126]['UKV_QH']['surf_centre_diff'].iloc[
    np.where(DOY_dict[2016126]['UKV_QH']['surf_centre_diff'] == DOY_dict[2016126]['UKV_QH']['surf_centre_diff'].min())[
        0]])
print(123, ': ', DOY_dict[2016123]['UKV_QH']['surf_centre_diff'].iloc[
    np.where(DOY_dict[2016123]['UKV_QH']['surf_centre_diff'] == DOY_dict[2016123]['UKV_QH']['surf_centre_diff'].min())[
        0]])


# Looking at % difference in fluxes at two heights
DOY_dict[2016126]['UKV_QH']['surf_lev_diff'] = ((DOY_dict[2016126]['UKV_QH'][13] - DOY_dict[2016126]['UKV_QH']['BL_H']) / DOY_dict[2016126]['UKV_QH'][13])*100
DOY_dict[2016123]['UKV_QH']['surf_lev_diff'] = ((DOY_dict[2016123]['UKV_QH'][13] - DOY_dict[2016123]['UKV_QH']['BL_H']) / DOY_dict[2016123]['UKV_QH'][13])*100
# mean percentage difference
print(' ')
print('MEAN % DIFFERENCE')
print(126, ': ', DOY_dict[2016126]['UKV_QH']['surf_lev_diff'].mean())
print(123, ': ', DOY_dict[2016123]['UKV_QH']['surf_lev_diff'].mean())
# max
print(' ')
print('MAX % DIFFERENCE')
print(126, ': ', DOY_dict[2016126]['UKV_QH']['surf_lev_diff'].iloc[np.where(DOY_dict[2016126]['UKV_QH']['surf_lev_diff'] == DOY_dict[2016126]['UKV_QH']['surf_lev_diff'].max())[0]])
print(123, ': ', DOY_dict[2016123]['UKV_QH']['surf_lev_diff'].iloc[np.where(DOY_dict[2016123]['UKV_QH']['surf_lev_diff'] == DOY_dict[2016123]['UKV_QH']['surf_lev_diff'].max())[0]])
# min
print(' ')
print('MIN % DIFFERENCE')
print(126, ': ', DOY_dict[2016126]['UKV_QH']['surf_lev_diff'].iloc[np.where(DOY_dict[2016126]['UKV_QH']['surf_lev_diff'] == DOY_dict[2016126]['UKV_QH']['surf_lev_diff'].min())[0]])
print(123, ': ', DOY_dict[2016123]['UKV_QH']['surf_lev_diff'].iloc[np.where(DOY_dict[2016123]['UKV_QH']['surf_lev_diff'] == DOY_dict[2016123]['UKV_QH']['surf_lev_diff'].min())[0]])
# """