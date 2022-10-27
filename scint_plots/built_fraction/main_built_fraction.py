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

    # combine obs with land cover csv obtained using the SAs
    df = built_fraction_funs.add_lc_to_df(df)


    DOY_dict[DOY] = {'obs': df}

    # get model sensible heat
    ukv_data_dict_QH = retrieve_model_fluxes.retrieve_UKV(scint_path, DOY, DOY, variable='H')
    UKV_df_QH = retrieve_model_fluxes.UKV_df(ukv_data_dict_QH)
    DOY_dict[DOY]['UKV_QH'] = UKV_df_QH

    # get model kdown
    ukv_data_dict_kdown = retrieve_model_fluxes.retrieve_UKV(scint_path, DOY, DOY, variable='kdown')
    UKV_df_kdown = retrieve_model_fluxes.UKV_df(ukv_data_dict_kdown)
    DOY_dict[DOY]['UKV_kdown'] = UKV_df_kdown

    # get model land cover
    # ToDo: Sort a script to handle retrieving and weighting lc data from the UKV
    lc_df = ukv_landuse.weight_lc_fractions(model_site_dict, percentage_vals_dict, DOY)




built_fraction_funs.plot_built_fraction(DOY_dict)

print('end')
