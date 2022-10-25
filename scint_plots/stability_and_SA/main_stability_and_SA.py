from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up

from scint_plots.stability_and_SA import stability_and_SA_funs

scint_path = 12
DOY_list = [2016126, 2016123]
var_list = ['z_0', 'z_d', 'z_f', 'sa_area_km2', 'ustar', 'stab_param']
time_res = '1min_sa10min'

pair_id = look_up.scint_path_numbers[scint_path]

DOY_dict = {}

# read the 60-min SA vars
for DOY in DOY_list:
    DOY_dict[DOY] = {}
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res='1min')
    DOY_dict[DOY]['1min'] = df

# read the 10-min SA vars
for DOY in DOY_list:
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res=time_res)

    DOY_dict[DOY][time_res] = df

# plot
stability_and_SA_funs.stability_and_sa(DOY_dict)
print('end')
