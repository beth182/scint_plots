# imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

mpl.rcParams.update({'font.size': 15})

from scint_plots.tools.preprocessed_scint_csvs import read_obs_csvs
from scint_plots.tools.preprocessed_UKV_csvs import read_UKV_csvs

# user choice
scint_path = 12
list_of_vars = ['QH', 'wind_direction_corrected', 'z_d', 'kdown', 'z_f', 'stab_param', 'L', 'ustar', 'wind_speed_adj',
                'qstar', 'sa_area_km2', 'z_0', 't_air', 'press_adj', 'r_h']
# z_f, QH, wind_direction_corrected, kdown, stab_param, L, ustar, wind_speed_adj, qstar, sa_area_km2, z_d, z_0, t_air, press_adj, r_h

list_of_model_vars = ['BL_H', 'kdown', 'wind_speed', 'wind_direction']
# time,BL_H,kdown,wind_speed,wind_direction

save_path = os.getcwd().replace('\\', '/') + '/'

list_of_vars_model_path = []
for item in list_of_model_vars:
    list_of_vars_model_path.append(item + '_' + str(scint_path))

list_of_vars_path = []
for item in list_of_vars:
    list_of_vars_path.append(item + '_' + str(scint_path))

# read the premade scint data csv files
obs_df = read_obs_csvs.read_all_of_preprocessed_scint_csv(list_of_vars, average=60)[list_of_vars_path]

# read model
df_UKV = read_UKV_csvs.read_all_of_preprocessed_UKV_csv(list_of_model_vars, model_level=0, grid_priority='primary')[
    list_of_vars_model_path]

# rename model columns
for col in list_of_vars_model_path:
    # col without the path characters
    var_name = col[:-3]
    if var_name == 'BL_H':
        var_name = 'QH'
    df_UKV = df_UKV.rename(columns={col: 'UKV_' + var_name})

# rename obs columns
for col in list_of_vars_path:
    # col without the path characters
    var_name = col[:-3]
    if var_name == 'wind_direction_corrected':
        var_name = 'wind_direction'
    if var_name == 'wind_speed_adj':
        var_name = 'wind_speed'
    if var_name == 'press_adj':
        var_name = 'press'
    obs_df = obs_df.rename(columns={col: var_name})

df = pd.concat([obs_df, df_UKV], axis=1).dropna()

# take the absolute difference
df['AE'] = np.abs(df['QH'] - df['UKV_QH'])

df['kdown_ratio'] = df['UKV_kdown'] / df['kdown']
df['QH_ratio'] = df['UKV_QH'] / df['QH']

# df = df[np.abs(df['kdown_ratio']) < 5]
# df = df[np.abs(df['QH_ratio']) < 5]


# ToDo: is any of this actually going to be used in the analysis? if not - move somehwere else



# """
# what to colour by
# colourbar = 'time'
# colourbar = 'AE'
colourbar = 'wind_direction'

inner_definition = 0.3

inners = df[df['QH_ratio'].between(1-inner_definition, 1+inner_definition, inclusive=True)][df['kdown_ratio'].between(1-inner_definition, 1+inner_definition, inclusive=True)]

# inners = df[np.abs(df['QH_ratio']) <= 0.8][np.abs(df['kdown_ratio']) <= 0.8]
outers_QH = df[~df['QH_ratio'].between(1-inner_definition, 1+inner_definition, inclusive=True)]
outers_Kdn = df[~df['kdown_ratio'].between(1-inner_definition, 1+inner_definition, inclusive=True)]

outers = pd.concat([outers_QH, outers_Kdn]).drop_duplicates()

assert len(outers) + len(inners) == len(df)


df_dict = {'outers':outers, 'inners':inners}

for key in df_dict.keys():

    df = df_dict[key]

    plt.figure(figsize=(10, 7))

    cm = plt.cm.get_cmap('gist_rainbow')

    plt.hlines(y=1, xmin=-10, xmax=10, linewidth=1, color='k')
    plt.vlines(x=1, ymin=-10, ymax=10, linewidth=1, color='k')

    if colourbar == 'time':
        ye = plt.scatter(df.QH_ratio, df.kdown_ratio, marker='.', c=df.index.hour, cmap=cm)
        cbar_lab = 'time of day (hour)'
    elif colourbar == 'wind_direction':

        bounds = np.linspace(0, 360, int(360/ 30)+1)
        norm = mpl.colors.BoundaryNorm(bounds, cm.N)
        ye = plt.scatter(df.QH_ratio, df.kdown_ratio, marker='.', c=df[colourbar], cmap=cm, norm=norm)
        cbar_lab = colourbar

    else:
        ye = plt.scatter(df.QH_ratio, df.kdown_ratio, marker='.', c=df[colourbar], cmap=cm)
        cbar_lab = colourbar

    cbar = plt.colorbar(ye)
    cbar.set_label(cbar_lab)

    plt.ylabel('Kdn mod / Kdn obs')
    plt.xlabel('QH mod / QH obs')

    # plt.ylim(df.kdown_ratio.min() - 0.2, df.kdown_ratio.max() +0.2)
    # plt.xlim(df.QH_ratio.min() - 0.2, df.QH_ratio.max() +0.2)

    if key == 'outers':

        plt.ylim(0, 4.5)
        plt.xlim(-1, 3.5)
    elif key == 'inners':
        plt.ylim(1-inner_definition - 0.1, 1+inner_definition + 0.1)
        plt.xlim(1-inner_definition - 0.1, 1+inner_definition + 0.1)

    plt.text(0.02, 0.95, "N = " + str(len(df)), transform=plt.axes().transAxes)

    plt.tight_layout()

    # plt.show()
    plt.savefig(save_path + colourbar + '_' + key + '.png', dpi=300, bbox_inches='tight')
# """


# initial scatter plots with colours set for worst and best 10%
"""
target_percentage = 10

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
