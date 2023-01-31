# Beth Saunders 31/01/2023
# script to produce a scatter plot of QH from 2 paths

# imports
import pandas as pd

# read in locally saved files
path_list = [11, 12, 13, 15]

path_df_dict = {}
for path in path_list:
    df = pd.read_csv('./path_' + str(path) + '_vals.csv')
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
    df = df.set_index('time')

    # just take the QH col
    df_qh = df[['QH']]
    # rename QH col to be the path + QH
    df_qh = df_qh.rename(columns={'QH': 'QH_' + str(path)})

    # append to dict
    path_df_dict[path] = df_qh

# combine all paths into one df
df_combine = pd.concat([path_df_dict[11], path_df_dict[12], path_df_dict[13], path_df_dict[15]], axis=1)

print('end')
