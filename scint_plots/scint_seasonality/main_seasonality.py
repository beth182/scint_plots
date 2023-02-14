# imports
import os

from scint_plots.tools.preprocessed_scint_csvs import read_obs_csvs
from scint_plots.scint_seasonality import seasonality_funs

# user choices
path_choice = 13

save_path = os.getcwd().replace('\\', '/') + '/'

# read the premade scint data csv files
df = read_obs_csvs.read_all_of_preprocessed_scint_csv(['QH'])

# drop any path other than the one chosen and BCT_IMU
for col in df.columns:
    if path_choice == int(col.split('_')[-1]):
        pass
    elif int(col.split('_')[-1]) == 12:
        pass
    else:
        df = df.drop(columns=[col])

# drop nans
df = df.dropna()

# split df into seasons
season_dict = seasonality_funs.split_df_into_season(df)

# seasonality_funs.plot_season(season_dict, save_path)
seasonality_funs.plot_season_one_panel(season_dict, save_path)

print('end')
