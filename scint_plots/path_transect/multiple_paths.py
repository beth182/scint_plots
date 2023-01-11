# Beth Saunders 11/01/23
# script to build upon existing functions to create a path transect figure for the 4 paths in the longer-term eval paper

# imports
import copy
import os
import matplotlib.pyplot as plt
from matplotlib import gridspec

import scintools as sct
from scintools.utils import path_weight
from scint_plots.path_transect import path_transect_funs

bdsm_path = 'D:/Documents/scintools/example_inputs/rasters/height_surface_4m.tif'
dem_path = 'D:/Documents/scintools/example_inputs/rasters/height_terrain_4m.tif'

save_path = os.getcwd().replace('\\', '/') + '/'

# construct paths in scintools
path_12_raw = sct.ScintillometerPair(x=[285440.6056, 284562.3107],
                                     y=[5712253.017, 5712935.032],
                                     z_asl=[142, 88],
                                     pair_id='BCT_IMU',
                                     crs='epsg:32631')

path_11_raw = sct.ScintillometerPair(x=[282251.14, 285440.6056],
                                     y=[5712486.47, 5712253.017],
                                     z_asl=[180, 142],
                                     pair_id='BTT_BCT',
                                     crs='epsg:32631')

path_13_raw = sct.ScintillometerPair(x=[284562.3107, 282251.14],
                                     y=[5712935.032, 5712486.47],
                                     z_asl=[88, 180],
                                     pair_id='IMU_BTT',
                                     crs='epsg:32631')

path_15_raw = sct.ScintillometerPair(x=[284450.1944, 285407],
                                     y=[5708094.734, 5708599.83],
                                     z_asl=[51, 44],
                                     pair_id='SCT_SWT',
                                     crs='epsg:32631')

path_12 = copy.deepcopy(path_12_raw)
path_11 = copy.deepcopy(path_11_raw)
path_13 = copy.deepcopy(path_13_raw)
path_15 = copy.deepcopy(path_15_raw)

path_dict = {'BCT_IMU': path_12, 'BTT_BCT': path_11, 'IMU_BTT': path_13, 'SCT_SWT': path_15}

transect_dict = {}
path_lengths = {}
pt_tallest_elements = {}
for path in path_dict.keys():
    # lengths
    path_lengths[path] = path_dict[path].path_length()

    # transects
    pt = path_transect_funs.path_transect(path_dict[path], bdsm_path, dem_path, 10)
    transect_dict[path] = pt

    # tallest elements
    pt_tallest_elements[path] = max(pt.gdf["z_asl_max_bdsm"])

# which path is the longest?
max_length = path_lengths[max(path_lengths, key=path_lengths.get)]

# which path has the highest element
max_height = pt_tallest_elements[max(pt_tallest_elements, key=pt_tallest_elements.get)]

num_of_paths = len(path_dict)

# plot
fig = plt.figure(constrained_layout=True, figsize=(10, 14))
spec = gridspec.GridSpec(ncols=1, nrows=num_of_paths)

count = 0

# ToDo: add to function input
# set order of plots by hard-entering the key order
# top = first, bottom = last
path_list = ['IMU_BTT', 'BCT_IMU', 'BTT_BCT', 'SCT_SWT']
pw_fun = sct.path_weight.bessel_approx
colour_dict = {'BCT_IMU': 'red', 'SCT_SWT': 'mediumorchid', 'IMU_BTT': 'green', 'BTT_BCT': 'blue'}

for i, path in enumerate(path_list):

    ax = fig.add_subplot(spec[i])

    ax.set_xlim(0 - 10, max_length + 10)
    ax.set_ylim(0, max_height + 5)

    pt = transect_dict[path]

    # plot the path weighting curve
    path_weight_df = path_weight.path_weight(fx=pw_fun, n_x=pt.gdf.shape[0])

    ax_t = ax.twinx()

    pw_line = ax_t.plot(pt.gdf.index * pt.point_res, path_weight_df["path_weight"], color="cornflowerblue",
                        linestyle='--',
                        label='Path weighting function')

    ax.spines['right'].set_color('cornflowerblue')
    ax_t.spines['right'].set_color('cornflowerblue')
    ax_t.yaxis.label.set_color('cornflowerblue')
    ax_t.tick_params(axis='y', colors='cornflowerblue')

    ax_t.set_ylim(0, 1)

    if i != 0:
        plt.setp(ax_t.get_yticklabels()[-1], visible=False)

    if i == len(path_dict) - 1:
        ax.set_xlabel('Horizontal distance (m)')
    else:
        ax.set_xticks([])
        plt.setp(ax.get_yticklabels()[0], visible=False)

    bld_line = ax.plot(pt.gdf.index * pt.point_res, pt.gdf["z_asl_max_bdsm"], color='dimgrey', label='Building heights')
    ground_line = ax.plot(pt.gdf.index * pt.point_res, pt.gdf["z_asl_max_dem"], color='sienna', label='Ground height')

    ax.fill_between(pt.gdf.index * pt.point_res, pt.gdf["z_asl_max_bdsm"], pt.gdf["z_asl_max_dem"], color='grey',
                    alpha=0.5)
    ax.fill_between(pt.gdf.index * pt.point_res, 0, pt.gdf["z_asl_max_dem"], color='sienna', alpha=0.5)

    # plot the path
    path_line = ax.plot(pt.gdf.path_length_m, pt.gdf["path_height_asl"], color=colour_dict[path], label=path)

    # add effective beam height label
    ebh = pt.effective_beam_height()
    plt.text(0.89, 0.8, '$z_{fb}$ = %d.2 m agl' % ebh, horizontalalignment='center', transform=ax.transAxes,
             color='lime')
    ax.plot(pt.gdf.path_length_m, ebh + pt.gdf["z_asl_max_dem"], color='lime', linestyle=':')

    # label of path
    plt.text(0.9, 0.9, str(path.split('_')[0] + r' $\rightarrow$ ' + path.split('_')[1]), horizontalalignment='center',
             transform=ax.transAxes, color=colour_dict[path])

    plt.subplots_adjust(wspace=0, hspace=0)

fig.text(0.06, 0.5, 'Height asl (m)', va='center', rotation='vertical')
fig.text(0.95, 0.5, 'Path Weighting', va='center', rotation='vertical', color='cornflowerblue')

plt.savefig(save_path + 'multiple_path_transect.png', bbox_inches='tight', dpi=300)

print('end')
