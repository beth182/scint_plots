from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up

from scint_plots.line_time_series import line_time_series_funs

scint_path = 12
DOY_list = [2016126, 2016123]
var_list = ['QH', 'kdown']
time_res = '1min_sa10min'

pair_id = look_up.scint_path_numbers[scint_path]

DOY_dict = {}

for DOY in DOY_list:

    # 1
    df_1 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                               pair_id=pair_id,
                                               var_list=var_list,
                                               time_res='1min_sa10min' + '_PERIOD_VAR_' + str(1))

    # 2
    df_2 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                               pair_id=pair_id,
                                               var_list=var_list,
                                               time_res='1min_sa10min' + '_PERIOD_VAR_' + str(2))

    # 3
    df_3 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                               pair_id=pair_id,
                                               var_list=var_list,
                                               time_res='1min_sa10min' + '_PERIOD_VAR_' + str(3))

    # 5
    df_5 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                               pair_id=pair_id,
                                               var_list=var_list,
                                               time_res='1min_sa10min' + '_PERIOD_VAR_' + str(5))

    # 10
    df_10 = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                                pair_id=pair_id,
                                                var_list=var_list,
                                                time_res='1min_sa10min' + '_PERIOD_VAR_' + str(10))

    DOY_dict[DOY] = {'1': df_1, '2': df_2, '3': df_3, '5': df_5, '10': df_10}

line_time_series_funs.times_series_line_QH_KDOWN_REVIEW_EXAMPLE(DOY_dict, pair_id)

print('end')
