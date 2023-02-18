import pandas as pd

from scint_flux.functions import read_calculated_fluxes
from scint_flux import look_up
from scint_flux.beth_temp.peak_analysis import peak_analysis

scint_path = 12

# DOY_list = [2016126, 2016123]
DOY_list = [2016134, 2016103]

"""
# read in csv with days
DOY_df = pd.read_csv('C:/Users/beths/OneDrive - University of Reading/Paper 2/categorize_days/days_to_be_read_in.csv')
# take only days of the target path
scint_path_string = 'P' + str(scint_path)
df_subset = DOY_df.iloc[np.where(DOY_df[scint_path_string] == 1)[0]]
df_subset['DOY_string'] = df_subset.year.astype(str) + df_subset.DOY.astype(str)
df_subset['DOY_string'] = df_subset['DOY_string'].astype(int)
DOY_list = df_subset.DOY_string.to_list()
"""

var_list = ['QH', 'kdown']

# time_res = '1min_sa10min'
# time_res = '1min'
time_res = '1min_sa10_mins_ending'

pair_id = look_up.scint_path_numbers[scint_path]

DOY_dict = {}

df_list = []

for DOY in DOY_list:
    # read the observations
    df = read_calculated_fluxes.extract_data(doy_list=[DOY],
                                             pair_id=pair_id,
                                             var_list=var_list,
                                             time_res=time_res)

    DOY_dict[DOY] = {time_res: df}

    # model data
    # retrieve BL_H
    ukv_data_dict_BL_H = retrieve_model_fluxes.retrieve_UKV(scint_path, DOY, DOY, variable='BL_H')
    UKV_df_BL_H = retrieve_model_fluxes.UKV_df(ukv_data_dict_BL_H)
    # retrieve kdown
    ukv_data_dict_kdown = retrieve_model_fluxes.retrieve_UKV(scint_path, DOY, DOY, variable='kdown', sa_analysis=False)
    UKV_df_kdown = retrieve_model_fluxes.UKV_df(ukv_data_dict_kdown)

    # combine model df
    UKV_df = pd.concat([UKV_df_BL_H, UKV_df_kdown], axis=1).rename(columns={'13': 'kdown_UKV', 'BL_H_13': 'BL_H_UKV'})

    peak_df = peak_analysis.peak_BE(df, UKV_df, pair_id)

    df_list.append(peak_df)

    print('end')

peak_df = pd.concat(df_list)
# save csv
# peak_df.to_csv('C:/Users/beths/OneDrive - University of Reading/Paper 2/categorize_days/peak_analysis/peak_analysis_' + pair_id +'.csv')

# plot
peak_analysis.peak_analysis_plot(peak_df)

print('end')
