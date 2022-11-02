from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up

from scint_plots.sa_frequency import sa_frequency_funs

scint_path = 12
DOY_list = [2016126, 2016123]
var_list = ['QH']
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
    DOY_dict[DOY] = {time_res: df}

# read the 60-min SA vars
for DOY in DOY_list:
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res='1min')

    DOY_dict[DOY]['1min'] = df

# plot
sa_frequency_funs.setup_sa_frequency(DOY_dict)
print('end')
