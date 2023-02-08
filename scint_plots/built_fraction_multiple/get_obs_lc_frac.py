# Beth Saunders 07/02/23
# Script to read and write csvs of land cover fractions in observation source areas

# imports
import pandas as pd
import numpy as np
import datetime as dt
import os

from scint_flux import look_up
from scint_fp.functions.sa_lc_fractions import lc_fractions_in_sa

# user choices
scint_path = 13

save_path = os.getcwd().replace('\\', '/') + '/'
# read in all files
# read in csv with days
DOY_df = pd.read_csv(save_path + 'days_to_be_read_in.csv')
# DOY_df = pd.read_csv('C:/Users/beths/OneDrive - University of Reading/Paper 2/days_to_be_read_in.csv')
# DOY_df = pd.read_csv('C:/Users/beths/OneDrive - University of Reading/Paper 2/all_days.csv')

# take only days of the target path
scint_path_string = 'P' + str(scint_path)
df_subset = DOY_df.iloc[np.where(DOY_df[scint_path_string] == 1)[0]]
df_subset['DOY_string'] = df_subset.year.astype(str) + df_subset.DOY.astype(str)
df_subset['DOY_string'] = df_subset['DOY_string'].astype(int)
DOY_list = df_subset.DOY_string.to_list()

pair_id = look_up.scint_path_numbers[scint_path]

# base_sa_dir = '//rdg-home.ad.rdg.ac.uk/research-nfs/basic/micromet/Tier_processing/rv006011/PycharmProjects/scintillometer_footprints/scint_fp/test_outputs/10_mins_ending/'
base_sa_dir = '/storage/basic/micromet/Tier_processing/rv006011/PycharmProjects/scintillometer_footprints/scint_fp/test_outputs/10_mins_ending/'

# get DOY list into directory format for the SA location
for year_DOY in DOY_list:

    # split into year and doy - as zfill on doy's with less than 3 digits is an issue
    dt_obj = dt.datetime.strptime(str(year_DOY), '%Y%j')

    DOY_str = dt_obj.strftime('%j')
    year_str = dt_obj.strftime('%Y')

    dir_path = base_sa_dir + year_str + DOY_str + '/'

    DOY_sa_files = [dir_path + filename for filename in os.listdir(dir_path) if
                    filename.startswith(pair_id) and filename.endswith('.tif')]

    # read each and extract fractions for this day
    df_doy = lc_fractions_in_sa.lc_fract_multiple_sas(sa_list=DOY_sa_files, save_path=save_path, landcover_location=save_path+'LandUseMM_7classes_32631.tif')

    # make sure the df is in chronological order
    df_doy = df_doy.sort_index()

    # save csv for given day
    save_dir_csv = save_path + 'sa_lc_fractions/' + str(pair_id) + '/'
    if not os.path.exists(save_dir_csv):
        os.makedirs(save_dir_csv)
    csv_file_name = pair_id + '_' + year_str + DOY_str + '_weighted_sa_lc.csv'
    file_path_out = save_dir_csv + csv_file_name

    df_doy.to_csv(file_path_out)

print('end')
