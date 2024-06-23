# creates a set of footprints from experimenal branch of scintools - where there is only one eddy covariance footprint
# calculated at the centre of the path. This set will then be compared to the existing SAs.
# This is in answer to the examiners' point:

# Flow dependent roughness length, effective measurement height, and varying source areas are well justified
# theoretically in the thesis. However, a quantitative assessment of the impact of these extensions is lacking.
# How big are the changes by the newly developed methodology to the previously used workflow? Adding quantitative
# results from sensitivity experiments in chapter 2 will strengthen the thesis and make the progress
# more visible and valuable.

# scintools branch name: impacts_of_pointfp

# note this is copied over from scintools & therefore file paths are likely to be incorrect.

import os
import pandas as pd
import scintools as sct
import numpy as np
import copy
import matplotlib.pyplot as plt

bdsm_path = 'D:/Documents/scintools/example_inputs/rasters/height_surface_4m.tif'
cdsm_path = 'D:/Documents/scintools/example_inputs/rasters/height_veg_4m.tif'
dem_path = 'D:/Documents/scintools/example_inputs/rasters/height_terrain_4m.tif'

# path 12 - BCT -> IMU
pair_raw = sct.ScintillometerPair(x=[285440.6056, 284562.3107],
                                  y=[5712253.017, 5712935.032],
                                  z_asl=[142, 88],
                                  pair_id='BCT_IMU',
                                  crs='epsg:32631')

pair = copy.deepcopy(pair_raw)

roughness_inputs = sct.RoughnessInputs()

spatial_inputs = sct.SpatialInputs(
    domain_size=15000,
    x=float(pair.path_center().x),
    y=float(pair.path_center().y),
    z_asl=pair.path_center_z(),
    bdsm_path=bdsm_path,
    cdsm_path=cdsm_path,
    dem_path=dem_path)

point_res = 50  # suplicate every 50 m
weightings = (100, 200)  # defult
path_params = {'point_res': point_res,
               'weightings': weightings}


current_dir = os.getcwd().replace('\\', '/') + '/'
out_dir = current_dir + 'outputs/'

# read in input csv
csv_name = 'met_inputs_' + 'hourly' + '_' + '123' + '.csv'
csv_path = current_dir + csv_name
assert os.path.isfile(csv_path)

# read inputs csv
df = pd.read_csv(csv_path)
df.rename(columns={'Unnamed: 0': 'time'}, inplace=True)
df.time = pd.to_datetime(df['time'], dayfirst=False)
df = df.set_index('time')

# create footprint for each entry in dataframe
for index, row in df.iterrows():
    time = row.name
    sigv = row['sig_v']
    wd = row['wind_direction_convert']
    ustar = row['ustar']
    L = row['L']

    title_string = time.strftime('%Y') + '_' + time.strftime('%j') + '_' + time.strftime('%H_%M')

    print(' ')
    print(title_string)
    print(' ')

    met_inputs = sct.MetInputs(obukhov=L,
                               sigv=sigv,
                               ustar=ustar,
                               wind_dir=wd
                               )

    fp_path = sct.run_pathfootprint(scint_pair=pair,
                                    met_inputs=met_inputs,
                                    roughness_inputs=roughness_inputs,
                                    path_params=path_params,
                                    target_percentage=0.6,
                                    spatial_inputs=spatial_inputs,
                                    method_test=True)


    fp_path.roughness_outputs.z_m = -999.0
    fp_path.footprint[fp_path.footprint == 0.0] = np.nan

    string_to_save = str(pair.pair_id) + '_' + str(spatial_inputs.domain_size) + '_' + title_string
    file_out = out_dir + string_to_save + '.tif'
    fp_path.save(out_dir + string_to_save)
    fp_path.save_tiff(file_out)

    print('saved: ', file_out)

print('end')
