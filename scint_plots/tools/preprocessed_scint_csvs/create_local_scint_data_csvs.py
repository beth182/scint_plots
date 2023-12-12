# Beth Saunders 31/01/2023
# Script which creates local csv files with path data

# imports
import pandas as pd
import os

from scint_flux.functions import read_calculated_fluxes


# re-run here if I am needing to re-write obs csv
def save_df_to_csv(save_path='./',
                   average=60,
                   offset=0,
                   all_days=True,
                   **kwargs):
    """

    :return:
    """

    csv_in_path = 'C:/Users/beths/OneDrive - University of Reading/Paper 2/all_days.csv'
    df_in = pd.read_csv(csv_in_path)
    df_in['DOY_string'] = (df_in.year.astype(str) + df_in.DOY.astype(str).str.zfill(3)).astype(int)


    if all_days == False:
        # Make sure the target DOY is included in kwargs
        assert 'DOY' in kwargs.keys()
        target_DOY = kwargs['DOY']

        df_in = df_in[df_in.DOY_string == target_DOY]

        # make sure that the target DOY was in the all das df
        assert len(df_in) == 1

    df_dict = {'13': [], '12': [], '11': [], '15': []}

    list_of_vars = ['QH', 'wind_direction_corrected', 'kdown', 'stab_param', 'L', 'ustar', 'wind_speed_adj', 'qstar',
                    'sa_area_km2', 'z_d', 'z_0', 't_air', 'press_adj', 'r_h']

    for i, row in df_in.iterrows():

        print(int(row.DOY_string))

        if all_days == True:
            hour_ending = True
        else:
            hour_ending = False


        if row.P13 == 1:
            df_13 = read_calculated_fluxes.extract_data([int(row.DOY_string)], pair_id='IMU_BTT',
                                                        var_list=list_of_vars,
                                                        time_res= '1min_sa10_mins_ending_PERIOD_VAR_' + str(average),
                                                        hour_ending=hour_ending)

            df_dict['13'].append(df_13)

        if row.P11 == 1:
            df_11 = read_calculated_fluxes.extract_data([int(row.DOY_string)], pair_id='BTT_BCT',
                                                        var_list=list_of_vars,
                                                        time_res='1min_sa10_mins_ending_PERIOD_VAR_' + str(average),
                                                        hour_ending=hour_ending)
            df_dict['11'].append(df_11)

        if row.P12 == 1:
            df_12 = read_calculated_fluxes.extract_data([int(row.DOY_string)], pair_id='BCT_IMU',
                                                        var_list=list_of_vars,
                                                        time_res='1min_sa10_mins_ending_PERIOD_VAR_' + str(average),
                                                        hour_ending=hour_ending)
            df_dict['12'].append(df_12)

        if row.P15 == 1:
            df_15 = read_calculated_fluxes.extract_data([int(row.DOY_string)], pair_id='SCT_SWT',
                                                        var_list=list_of_vars,
                                                        time_res='1min_sa10_mins_ending_PERIOD_VAR_' + str(average),
                                                        hour_ending=hour_ending)
            df_dict['15'].append(df_15)



    if all_days == False:
        save_name = str(target_DOY) + '_' + str(average)
    else:
        save_name = str(average)

    for key in df_dict:

        if len(df_dict[key]) != 0:
            df_combine = pd.concat(df_dict[key])

            if offset == 0:
                df_combine.to_csv(save_path + 'path_' + key + '_' + save_name + '_vals.csv')

            else:
                save_path_offset = save_path + 'offset_' + str(offset) + '/'
                df_combine.to_csv(save_path_offset + 'path_' + key + '_' + save_name + '_vals.csv')



if __name__ == '__main__':
    save_path = os.getcwd().replace('\\', '/') + '/csv_files/'

    # all days data
    # """
    # save_df_to_csv(save_path, average=60)
    save_df_to_csv(save_path, average=10)
    # save_df_to_csv(save_path, average=15, offset=15)

    print('end')
    # """

    # 1-min average data for high-resolution days
    """
    save_df_to_csv(save_path, average=1, all_days=False, DOY=2016134)
    # save_df_to_csv(save_path, average=1, offset=15, all_days=False, DOY=2016134)
    """
    print('end')
