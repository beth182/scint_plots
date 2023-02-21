# imports
import datetime as dt
import pandas as pd


def read_all_of_preprocessed_scint_csv(list_of_vars=['QH'],
                                       csv_dir='D:/Documents/scint_plots/scint_plots/tools/preprocessed_scint_csvs/csv_files/',
                                       average=60,
                                       offset=0):
    """

    :return:
    """

    # read in locally saved files
    path_list = [11, 12, 13, 15]

    if offset == 0:
        pass
    else:
        csv_dir = csv_dir + 'offset_' + str(offset) + '/'

    path_df_dict = {}
    for path in path_list:
        df = pd.read_csv(csv_dir + 'path_' + str(path) + '_' + str(average) + '_vals.csv')
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


def read_selection_of_preprocessed_scint_csv(scint_path,
                                             DOY_list,
                                             save_path):
    """
    Take the subset of days from the pre made csvs with hourly obs data
    These csv's have been made to read in to save time (not read netCDF files on network mount)
    :param scint_path:
    :param DOY_list:
    :param save_path:
    :return:
    """
    # take the subset of days from the pre made csvs with hourly obs data - that have been read in to save time
    pre_made_csv_dir = save_path + '../path_comparison/'

    # select the target path
    path_data_filepath = pre_made_csv_dir + 'path_' + str(scint_path) + '_vals.csv'

    # read the csv
    scint_df = pd.read_csv(path_data_filepath)
    scint_df['time'] = pd.to_datetime(scint_df['time'], format='%Y-%m-%d %H:%M:%S')
    scint_df = scint_df.set_index('time')

    # take just the days in the DOY list
    df_DOY_list = []
    for DOY in DOY_list:
        dt_obj = dt.datetime.strptime(str(DOY), '%Y%j')
        next_day = dt_obj + dt.timedelta(days=1)

        mask = (scint_df.index >= dt_obj) & (scint_df.index < next_day)
        df_DOY = scint_df.loc[mask]

        df_DOY_list.append(df_DOY)

    df = pd.concat(df_DOY_list)

    return df
