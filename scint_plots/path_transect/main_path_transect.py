import copy

import scintools as sct

from scint_plots.path_transect import path_transect_funs


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


pt = path_transect_funs.path_transect(pair, bdsm_path, dem_path, 10)


path_transect_funs.transect_plot(pt, pw_fun=sct.path_weight.bessel_approx)
print('end')