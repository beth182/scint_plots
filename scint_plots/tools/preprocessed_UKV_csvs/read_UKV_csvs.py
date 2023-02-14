# imports
import pandas as pd

from scint_flux import look_up


def read_all_of_preprocessed_UKV_csv(list_of_vars=['BL_H'],
                                       csv_dir='D:/Documents/scint_plots/scint_plots/tools/preprocessed_UKV_csvs/UKVcsv_files/'):
    """

    :return:
    """

    # read in locally saved files
    path_list = [11, 12, 13, 15]

    path_df_dict = {}
    for path in path_list:
        pair_id = look_up.scint_path_numbers[path]
        df = pd.read_csv(csv_dir + 'path_' + str(path) + '_vals.csv')
        df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
        df = df.set_index('time')

        # just take the target cols
        df_qh = df[list_of_vars]
        # rename cols to be the path + var name
        for var in list_of_vars:
            df_qh = df_qh.rename(columns={var: var + '_' + str(path)})

        # append to dict
        path_df_dict[path] = df_qh

    # combine all paths into one df
    df_combine = pd.concat([path_df_dict[11], path_df_dict[12], path_df_dict[13], path_df_dict[15]], axis=1)

    return df_combine