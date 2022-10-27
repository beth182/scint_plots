from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up
from scint_eval.functions import retrieve_model_fluxes
from scint_plots.detailed_time_series import detailed_time_series_funs

scint_path = 12
DOY_list = [2016126, 2016123]
var_list = ['QH']
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

    # get model sensible heat
    # retrieve UKV data
    ukv_data_dict_QH = retrieve_model_fluxes.retrieve_UKV(scint_path, DOY, DOY, variable='H')
    UKV_df_QH = retrieve_model_fluxes.UKV_df(ukv_data_dict_QH)
    DOY_dict[DOY] = {'obs': df, 'UKV_QH': UKV_df_QH}

    detailed_time_series_funs.detailed_time_series(obs_df=df,
                                                   ukv_df=UKV_df_QH,
                                                   model_site_dict=ukv_data_dict_QH['model_site_dict'],
                                                   BL_H_z=ukv_data_dict_QH['BL_H_z'],
                                                   variable='H',
                                                   number_grids_axes=False
                                                   )

print('end')
