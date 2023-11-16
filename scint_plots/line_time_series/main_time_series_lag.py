import matplotlib.pyplot as plt
import numpy as np

from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up

from scint_plots.line_time_series import time_series_lag_funs

scint_path = 12
DOY_list = [2016126, 2016123]
var_list = ['QH', 'kdown']
time_res = '1min_sa10min' + '_PERIOD_VAR_' + str(1)

pair_id = look_up.scint_path_numbers[scint_path]

DOY_dict = {}

for DOY in DOY_list:
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res=time_res)


    time_series_lag_funs.ts_scatter_plot(df, pair_id, minute_displace=0)

    print('end')


    r_list = []
    displace_list = []

    for i in range(-100, 100):

        print(i)

        r = time_series_lag_funs.ts_scatter_plot(df, pair_id, minute_displace=i)
        displace_list.append(i)
        r_list.append(r)


    DOY_dict[DOY] = {'r_list': r_list, 'displace_list': displace_list}


index_126 = np.where(DOY_dict[2016126]['r_list'] == max(DOY_dict[2016126]['r_list']))[0][0]
index_123 = np.where(DOY_dict[2016123]['r_list'] == max(DOY_dict[2016123]['r_list']))[0][0]

plt.plot(DOY_dict[2016123]['displace_list'], DOY_dict[2016123]['r_list'], label='IOP-1: ' + str(DOY_dict[2016123]['displace_list'][index_123]), color='blue')
plt.plot(DOY_dict[2016126]['displace_list'], DOY_dict[2016126]['r_list'], label='IOP-2: ' + str(DOY_dict[2016126]['displace_list'][index_126]), color='orange')

plt.scatter(DOY_dict[2016123]['displace_list'][index_123], DOY_dict[2016123]['r_list'][index_123], color='blue')
plt.scatter(DOY_dict[2016126]['displace_list'][index_126], DOY_dict[2016126]['r_list'][index_126], color='orange')

plt.legend()


plt.ylabel('r')
plt.xlabel('# minutes $Q_{H,LAS}$ shifted')

dir_name = './'
plt.savefig(dir_name + pair_id + '_lag' + '.png', bbox_inches='tight', dpi=300)

print('end')