# Beth Saunders 31/01/2023
# Script which creates local csv files with path data

# imports
import pandas as pd
import os

from scint_flux.functions import read_calculated_fluxes


# re-run here if I am needing to re-write obs csv
def save_df_to_csv(save_path='./',
                   main_dir='//rdg-home.ad.rdg.ac.uk/research-nfs/basic/micromet/Tier_processing/rv006011/scint_data_testing/data/'):
    """

    :return:
    """

    csv_in_path = 'C:/Users/beths/OneDrive - University of Reading/Paper 2/all_days.csv'
    df_in = pd.read_csv(csv_in_path)
    df_in['DOY_string'] = (df_in.year.astype(str) + df_in.DOY.astype(str).str.zfill(3)).astype(int)

    df_dict = {'13': [], '12': [], '11': [], '15': []}

    list_of_vars = ['QH', 'wind_direction_corrected', 'kdown', 'stab_param', 'L', 'ustar', 'wind_speed_adj', 'qstar',
                    'sa_area_km2', 'z_d', 'z_0', 't_air', 'press_adj', 'r_h']

    for i, row in df_in.iterrows():

        print(int(row.DOY_string))

        if row.P13 == 1:
            df_13 = read_calculated_fluxes.extract_data([int(row.DOY_string)], pair_id='IMU_BTT',
                                                        var_list=list_of_vars, average=60, hour_ending=True)
            df_dict['13'].append(df_13)

        if row.P11 == 1:
            df_11 = read_calculated_fluxes.extract_data([int(row.DOY_string)], pair_id='BTT_BCT',
                                                        var_list=list_of_vars, average=60, hour_ending=True)
            df_dict['11'].append(df_11)

        if row.P12 == 1:
            df_12 = read_calculated_fluxes.extract_data([int(row.DOY_string)], pair_id='BCT_IMU',
                                                        var_list=list_of_vars, average=60, hour_ending=True)
            df_dict['12'].append(df_12)

        if row.P15 == 1:
            df_15 = read_calculated_fluxes.extract_data([int(row.DOY_string)], pair_id='SCT_SWT',
                                                        var_list=list_of_vars, average=60, hour_ending=True)
            df_dict['15'].append(df_15)

    df_combine_13 = pd.concat(df_dict['13'])
    df_combine_13.to_csv(save_path + 'path_13_vals.csv')

    df_combine_15 = pd.concat(df_dict['15'])
    df_combine_15.to_csv(save_path + 'path_15_vals.csv')

    df_combine_12 = pd.concat(df_dict['12'])
    df_combine_12.to_csv(save_path + 'path_12_vals.csv')

    df_combine_11 = pd.concat(df_dict['11'])
    df_combine_11.to_csv(save_path + 'path_11_vals.csv')


if __name__ == '__main__':
    save_path = os.getcwd().replace('\\', '/') + '/csv_files/'

    save_df_to_csv(save_path)
    print('end')
