import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({'font.size': 15})

from scint_flux import look_up

from scint_plots.peak_flux_performance import peak_funs

from scint_plots.tools.preprocessed_scint_csvs import read_obs_csvs
from scint_plots.tools.preprocessed_UKV_csvs import read_UKV_csvs
from scint_plots.scint_seasonality import seasonality_funs


# ToDo: do I need the statistics csvs anymore in FLUX_PLOTS


def peak_plot(path_dict, save_path):
    """

    Returns
    -------

    """

    colour_dict = {'BCT_IMU': 'red', 'SCT_SWT': 'mediumorchid', 'IMU_BTT': 'green', 'BTT_BCT': 'blue'}
    marker_dict = {'BCT_IMU': 'o', 'SCT_SWT': 'v', 'IMU_BTT': 's', 'BTT_BCT': '^'}

    plt.figure(figsize=(10, 6))

    x_ticks_manual = [-5.5, -3.5, -1.5, 0, 1.5, 3.5, 5.5]

    for pair_id in path_dict.keys():
        print(' ')
        print(pair_id)
        print(' ')

        df = path_dict[pair_id]

        print('len dt 5, 6: ', len(df[df['time_delta_qh'].between(5, 6)]))
        print('len dt 3, 4: ', len(df[df['time_delta_qh'].between(3, 4)]))
        print('len dt 1, 2: ', len(df[df['time_delta_qh'].between(1, 2)]))
        print('len dt 0: ', len(df[df['time_delta_qh'] == 0]))
        print('len dt -2, -1: ', len(df[df['time_delta_qh'].between(-2, -1)]))
        print('len dt -4, -3: ', len(df[df['time_delta_qh'].between(-4, -3)]))
        print('len dt -6, -5: ', len(df[df['time_delta_qh'].between(-6, -5)]))

        num_list = [len(df[df['time_delta_qh'].between(-6, -5)]), len(df[df['time_delta_qh'].between(-4, -3)]),
                    len(df[df['time_delta_qh'].between(-2, -1)]), len(df[df['time_delta_qh'] == 0]), len(
                df[df['time_delta_qh'].between(1, 2)]), len(df[df['time_delta_qh'].between(3, 4)]), len(
                df[df['time_delta_qh'].between(5, 6)])]

        plt.plot(x_ticks_manual, num_list, color=colour_dict[pair_id], alpha=0.3)
        plt.plot(x_ticks_manual, num_list, label=pair_id, color=colour_dict[pair_id], marker=marker_dict[pair_id],
                 linestyle='None')

    plt.legend()

    x_tick_labels = ['$-6\leq\Delta T\leq-5$', '$-4\leq\Delta T\leq-3$', '$-2\leq\Delta T\leq-1$', '$\Delta T=0$',
                     '$1\leq\Delta T\leq2$', '$3\leq\Delta T\leq4$', '$5\leq\Delta T\leq6$']

    plt.xticks(x_ticks_manual, x_tick_labels, rotation=45)

    plt.xlabel('Hours ($\Delta T$) difference between modelled and observed peak $Q_{H}$')
    plt.ylabel('Count')

    plt.savefig(save_path + 'peak_QH_timing.png', bbox_inches='tight', dpi=300)

    print('end')


# User inputs
# scint_path = 15
scint_path_list = [11, 12, 13, 15]
# scint_path_list = [11, 15]

var_list = ['QH', 'kdown']
obs_average = 60

save_path = os.getcwd().replace('\\', '/') + '/'

path_dict = {}

for scint_path in scint_path_list:

    pair_id = look_up.scint_path_numbers[scint_path]

    # replace the QH in var list with BL flux
    UKV_var_list = []
    for variable in var_list:
        if variable == 'QH':
            ukv_variable = 'BL_H'
        else:
            ukv_variable = variable
        UKV_var_list.append(ukv_variable)

    # read the premade scint data csv files
    df_all = read_obs_csvs.read_all_of_preprocessed_scint_csv(var_list)

    # read the premade UKV data csv files
    df_UKV_all = read_UKV_csvs.read_all_of_preprocessed_UKV_csv(UKV_var_list)

    # drop columns not the path choice or BCT-IMU
    df_obs = seasonality_funs.drop_unchosen_cols(scint_path, df_all).dropna()
    df_UKV = seasonality_funs.drop_unchosen_cols(scint_path, df_UKV_all).dropna()

    # rename UKV vars
    for col in df_UKV:
        if col == 'BL_H_' + str(scint_path):
            df_UKV = df_UKV.rename(columns={col: 'UKV_QH_' + str(scint_path)})
        else:
            df_UKV = df_UKV.rename(columns={col: 'UKV_' + col})

    # combine model and obs df
    df = pd.concat([df_obs, df_UKV], axis=1)

    peak_df = peak_funs.peak_BE(df=df, scint_path=scint_path)

    path_dict[pair_id] = peak_df

peak_plot(path_dict, save_path)
