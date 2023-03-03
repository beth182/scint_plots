# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({'font.size': 15})

from scint_plots.tools.preprocessed_scint_csvs import read_obs_csvs
from scint_plots.tools.preprocessed_UKV_csvs import read_UKV_csvs


# user choice
scint_path = 12
target_percentage = 10
list_of_vars = ['QH', 'wind_direction_corrected', 'z_d', 'kdown', 'z_f', 'stab_param', 'L', 'ustar', 'wind_speed_adj', 'qstar', 'sa_area_km2', 'z_0', 't_air']
# z_f, QH, wind_direction_corrected, kdown, stab_param, L, ustar, wind_speed_adj, qstar, sa_area_km2, z_d, z_0, t_air, press_adj, r_h


list_of_vars_path = []
for item in list_of_vars:
    list_of_vars_path.append(item + '_' + str(scint_path))

# read the premade scint data csv files
obs_df = read_obs_csvs.read_all_of_preprocessed_scint_csv(list_of_vars, average=60)[list_of_vars_path]

# read model
df_UKV = read_UKV_csvs.read_all_of_preprocessed_UKV_csv(['BL_H'], model_level=0, grid_priority='primary')[
    ['BL_H_' + str(scint_path)]]


df = pd.concat([obs_df, df_UKV], axis=1).dropna()

# take the absolute difference
df['AE'] = np.abs(df['QH_' + str(scint_path)] - df['BL_H_' + str(scint_path)])



"""
# get number of data for target percentage
target_percentage_number = int((len(df) / 100) * target_percentage)


sorted_df = df.sort_values('AE')

best_df = sorted_df.iloc[0:target_percentage_number]
worst_df = sorted_df.iloc[-target_percentage_number:]


test_param = 'wind_direction_corrected'

plt.figure(figsize=(10,10))
plt.scatter(df.AE, df[test_param + '_' + str(scint_path)], color='grey', alpha=0.6, marker='.')


plt.scatter(best_df.AE, best_df[test_param + '_' + str(scint_path)], color='green', marker='.', label='best ' + str(target_percentage) + '%')
plt.scatter(worst_df.AE, worst_df[test_param + '_' + str(scint_path)], color='red', marker='.', label='worst ' + str(target_percentage) + '%')

plt.legend()
plt.xlabel('QH Absolute error')
plt.ylabel(test_param)

plt.show()

"""

print('end')
