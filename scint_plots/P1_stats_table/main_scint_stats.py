# imports
from scint_flux import look_up
from scint_flux.functions import read_calculated_fluxes
from scint_plots.P1_stats_table import scint_stat_funs


# main script for running stat functions of P1: Results table

scint_path = 12
DOY_list = [2016123]

var_list = ['QH', 'kdown']

time_res = '1min_sa10min'
# time_res = '1min'

pair_id = look_up.scint_path_numbers[scint_path]

for DOY in DOY_list:
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res=time_res)


    scint_stat_funs.stats_of_the_obs_fluxes(df)

    print('end')