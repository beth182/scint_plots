# imports
import os

from scint_plots.tools.preprocessed_scint_csvs import read_obs_csvs
from scint_plots.scint_seasonality import seasonality_funs
from scint_plots.tools.preprocessed_UKV_csvs import read_UKV_csvs

# user choices
path_choice = 13

save_path = os.getcwd().replace('\\', '/') + '/'

# read the premade scint data csv files
df = read_obs_csvs.read_all_of_preprocessed_scint_csv(['QH'])

# read the premade UKV data csv files
df_UKV = read_UKV_csvs.read_all_of_preprocessed_UKV_csv(['BL_H'])

# drop columns not the path choice or BCT-IMU
df = seasonality_funs.drop_unchosen_cols(path_choice, df).dropna()
df_UKV = seasonality_funs.drop_unchosen_cols(path_choice, df_UKV).dropna()

# split df into seasons
season_dict = seasonality_funs.split_df_into_season(df)
season_dict_UKV = seasonality_funs.split_df_into_season(df_UKV)

# seasonality_funs.plot_season(season_dict, save_path)
seasonality_funs.plot_season_one_panel(season_dict, season_dict_UKV, save_path)

print('end')
