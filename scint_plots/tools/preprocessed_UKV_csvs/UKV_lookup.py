# where 1 = primary grid, 2 = secondary grid
scint_UKV_grid_choices = {'BCT_IMU': {1: 13, 2: 22},
                          'IMU_BTT': {1: 12, 2: 21},
                          'BTT_BCT': {1: 21, 2: 12},
                          'SCT_SWT': {1: 37, 2: 38}}

# dict with median effective measurement height (z_f) for each pair ID
scint_median_zf = {'BCT_IMU': 73.6, 'IMU_BTT': 103.3, 'BTT_BCT': 113.5, 'SCT_SWT': 32.4}

# Dict for model level heigths of closest model level to median zf (0), and one above / bellow (1/-1) rounded to the
# nearest meter
# used as a look up to find file names for model offline csv files
model_level_heights = {'BCT_IMU': {1: 89, 0: 63, -1: 43},
                       'IMU_BTT': {1: 137, 0: 103, -1: 77},
                       'BTT_BCT': {1: 137, 0: 103, -1: 77},
                       'SCT_SWT': {1: 63, 0: 36, -1: 16}
                       }
