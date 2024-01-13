import datetime as dt

from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up

from scint_plots.line_time_series import line_time_series_funs
from scint_plots.tools.preprocessed_UKV_csvs import read_UKV_csvs



scint_path = 12
DOY_list = [2016134]
var_list = ['QH', 'kdown']
time_res = '1min_sa10_mins_ending_PERIOD_VAR_10'

pair_id = look_up.scint_path_numbers[scint_path]

DOY_dict = {}

for DOY in DOY_list:

    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res=time_res)

    df_1_min = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res='1min_sa10_mins_ending_PERIOD_VAR_1')


    line_time_series_funs.times_series_line_QH_KDOWN_UM100(df, pair_id, UM_100=True, df_1_min=df_1_min)


print('end')
