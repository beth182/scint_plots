import pandas as pd


from scint_flux import look_up
from scint_flux.beth_temp.peak_analysis import peak_analysis

from scint_plots.tools.preprocessed_scint_csvs import read_obs_csvs
from scint_plots.tools.preprocessed_UKV_csvs import read_UKV_csvs
from scint_plots.scint_seasonality import seasonality_funs

# User inputs
scint_path = 12
var_list = ['QH', 'kdown']



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
df = seasonality_funs.drop_unchosen_cols(scint_path, df_all).dropna()
df_UKV = seasonality_funs.drop_unchosen_cols(scint_path, df_UKV_all).dropna()


# per day
peak_df = peak_analysis.peak_BE(df, UKV_df, pair_id)









# all days
peak_df = pd.concat(df_list)





# save csv
# peak_df.to_csv('C:/Users/beths/OneDrive - University of Reading/Paper 2/categorize_days/peak_analysis/peak_analysis_' + pair_id +'.csv')

# plot
peak_analysis.peak_analysis_plot(peak_df)

print('end')
