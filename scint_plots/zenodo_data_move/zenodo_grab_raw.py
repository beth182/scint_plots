import os
import pandas as pd
import shutil

from scint_flux.run_function import construct_path
from scint_flux.functions.find_files import find_files
import scint_flux.look_up

# read in CSV with days

pair_id = 'SCT_SWT'

raw_scint_path = '//rdg-home.ad.rdg.ac.uk/research-nfs/rds/micromet/Tier_raw/'

bdsm_path = 'D:/Documents/scintools/example_inputs/rasters/height_surface_4m.tif'
cdsm_path = 'D:/Documents/scintools/example_inputs/rasters/height_veg_4m.tif'
dem_path = 'D:/Documents/scintools/example_inputs/rasters/height_terrain_4m.tif'

current_dir = os.getcwd().replace('\\', '/') + '/'

days_csv_path = current_dir + pair_id + '_days.csv'

# check csv exists

assert os.path.isfile(days_csv_path)

days_df = pd.read_csv(days_csv_path)

days_df['YYYYDOY'] = days_df['Year'].astype(str) + days_df['DOY'].astype(str)

DOY_list = days_df['YYYYDOY'].to_list()

path_df = construct_path(pair_id, bdsm_path, cdsm_path, dem_path)
pair = path_df['pair']

raw_scint_files = find_files(site=pair.pair_id.split('_')[1],
                             instrument=scint_flux.look_up.pair_instruments[pair_id], level='raw',
                             main_dir=raw_scint_path, doy_list=DOY_list)

raw_files_list = raw_scint_files['file_paths']

for raw_file in raw_files_list:
    print(raw_file)
    shutil.copy(raw_file, 'D:/zenodo/P2 CASES/LAS_raw/')

print('end')
