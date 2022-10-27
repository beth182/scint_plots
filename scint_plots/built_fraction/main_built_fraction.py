from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up

from scint_eval.functions import retrieve_model_fluxes
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

    # get model sensible heat
    ukv_data_dict_QH = retrieve_model_fluxes.retrieve_UKV(scint_path, DOY, DOY, variable='H')
    UKV_df_QH = retrieve_model_fluxes.UKV_df(ukv_data_dict_QH)
    DOY_dict[DOY] = {'obs': df, 'UKV_QH': UKV_df_QH}

    # get model kdown


    # resample the observations
    """
    # resample the obs into 10 min averages
    QH_obs_avs = read_calculated_fluxes.time_averages_of_obs(df, 'QH', on_hour=True).rename(
        columns={'obs_1': 'QH_1', 'obs_5': 'QH_5', 'obs_10': 'QH_10', 'obs_60': 'QH_60'})

    kdown_obs_avs = read_calculated_fluxes.time_averages_of_obs(df, 'kdown', on_hour=True, for_model=True).rename(
        columns={'obs_1': 'kdown_1', 'obs_5': 'kdown_5', 'obs_10': 'kdown_10', 'obs_60': 'kdown_60'})
    """

print('end')
