import os
import pandas as pd
import shutil

from scint_flux.run_function import construct_path
from scint_flux.functions.find_files import find_files

bdsm_path = 'D:/Documents/scintools/example_inputs/rasters/height_surface_4m.tif'
cdsm_path = 'D:/Documents/scintools/example_inputs/rasters/height_veg_4m.tif'
dem_path = 'D:/Documents/scintools/example_inputs/rasters/height_terrain_4m.tif'

pair_id = 'BCT_IMU'

current_dir = os.getcwd().replace('\\', '/') + '/'
days_csv_path = current_dir + pair_id + '_days.csv'

assert os.path.isfile(days_csv_path)

days_df = pd.read_csv(days_csv_path)

days_df['YYYYDOY'] = days_df['Year'].astype(str) + days_df['DOY'].astype(str)

path_df = construct_path(pair_id, bdsm_path, cdsm_path, dem_path)
pair = path_df['pair']

for index, row in days_df.iterrows():

    rad_site = row['rad_site']
    doy = row['YYYYDOY']

    if rad_site == 'BTT' or rad_site == 'SUEWS':
        rad_time_res = '1min'
    else:
        rad_time_res = '5s'

    if rad_site == 'KSSW':
        rad_file_path = '//rdg-home.ad.rdg.ac.uk/research-nfs/rds/micromet/Tier_raw/'
    elif rad_site == 'BTT':
        rad_file_path = '//rdg-home.ad.rdg.ac.uk/research-nfs/rds/micromet/Tier_processing/rv006011/scint_data_testing/'

    rad_files = find_files(site=rad_site,
                           instrument='CNR4', level='L0',
                           main_dir=rad_file_path,
                           doy=doy,
                           time_res=rad_time_res)

    assert len(rad_files['file_paths']) == 1
    raw_file = rad_files['file_paths'][0]

    shutil.copy(raw_file, 'D:/zenodo/P2 CASES/CNR4_processed/')
    print(raw_file)

print('end')
