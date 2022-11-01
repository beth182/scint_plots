from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up

from scint_plots.model_levels import model_levels_funs

scint_path = 12
DOY_list = [2016123, 2016126]
var_list = []
time_res = '1min'

pair_id = look_up.scint_path_numbers[scint_path]

DOY_dict = {}

for DOY in DOY_list:
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res=time_res)

    model_levels_funs.model_data_at_heights(DOY, df)

print('end')
