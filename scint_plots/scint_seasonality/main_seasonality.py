# imports
import os

from scint_plots.tools.preprocessed_scint_csvs import read_obs_csvs
from scint_plots.scint_seasonality import seasonality_funs
from scint_plots.tools.preprocessed_UKV_csvs import read_UKV_csvs

# user choices
variable = 'kdown'

# 11, 13, 15
# not 12 - this is always included
path_list = [11, 13, 15]

if variable == 'QH':
    ukv_variable = 'BL_H'
else:
    ukv_variable = variable

save_path = os.getcwd().replace('\\', '/') + '/'

# read the premade scint data csv files
df_all = read_obs_csvs.read_all_of_preprocessed_scint_csv([variable])

# read the premade UKV data csv files
df_UKV_all = read_UKV_csvs.read_all_of_preprocessed_UKV_csv([ukv_variable])

for path_choice in path_list:
    # drop columns not the path choice or BCT-IMU
    df = seasonality_funs.drop_unchosen_cols(path_choice, df_all).dropna()
    df_UKV = seasonality_funs.drop_unchosen_cols(path_choice, df_UKV_all).dropna()

    # split df into seasons
    season_dict = seasonality_funs.split_df_into_season(df)
    season_dict_UKV = seasonality_funs.split_df_into_season(df_UKV)

    # seasonality_funs.plot_season(season_dict, save_path)
    seasonality_funs.plot_season_one_panel(season_dict, season_dict_UKV, save_path, variable=variable)

print('end')
