import pandas as pd
import os

from scint_flux import look_up

from scint_plots.peak_flux_performance import peak_funs

from scint_plots.tools.preprocessed_scint_csvs import read_obs_csvs
from scint_plots.tools.preprocessed_UKV_csvs import read_UKV_csvs
from scint_plots.scint_seasonality import seasonality_funs

# ToDo: do I need the statistics csvs anymore in FLUX_PLOTS

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

# plot
# peak_funs.peak_analysis_plot(path_dict, obs_average, save_path)

# stats
# peak_funs.peak_stats(path_dict)
peak_funs.peak_stats_by_season(path_dict)  # by season
print('end')
