import rasterio.plot
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import geopandas as gpd
import matplotlib.colors as colors

save_path = os.getcwd().replace('\\', '/') + '/'

sa_dir = save_path + 'sa_files_used/'

# deal with files
file_list = []
os.chdir(sa_dir)
for file in glob.glob("*.tif"):
    file_list.append(sa_dir + file)

raster0 = rasterio.open(file_list[0])
fig, ax = plt.subplots(figsize=(10, 10))

# plot lancover map
# ToDo: make this avail
landcover_location = 'C:/Users/beths/OneDrive - University of Reading/Model_Eval/QGIS/Elliott/LandUseMM_7classes_32631.tif'
landcover_raster = rasterio.open(landcover_location)

color_list_lc = ["white", "dimgrey", "lightgrey", "deepskyblue", "lawngreen", "darkgreen", "limegreen", "olive"]
# make a color map of fixed colors
cmap_lc = colors.ListedColormap(color_list_lc)
bounds_lc = [0, 1, 2, 3, 4, 5, 6, 7, 8]
norm_lc = colors.BoundaryNorm(bounds_lc, cmap_lc.N)

rasterio.plot.show(landcover_raster, ax=ax, cmap=cmap_lc, norm=norm_lc, interpolation='nearest', alpha=0.5)

ax.set_xlim(280664.2382130053, 287345.2889264111)
ax.set_ylim(5707707.90450454, 5713269.294785313)

# POINT
raster_point = rasterio.open(file_list[1])
raster_array_point = raster_point.read(1)
# make all 0 vals in array nan
raster_array_point[raster_array_point == 0.0] = np.nan
# force non-zero vals to be 1
bool_arr_point = np.ones(raster_array_point.shape)
# remove nans in bool array
nan_index_point = np.where(np.isnan(raster_array_point))
bool_arr_point[nan_index_point] = 0.0
# get location of max val
ind_max_2d_point = np.unravel_index(np.nanargmax(raster_array_point), raster_array_point.shape)[:]
max_coords_point = raster_point.xy(ind_max_2d_point[0], ind_max_2d_point[1])

# plot
rasterio.plot.show(bool_arr_point, transform=raster_point.transform, contour=True, contour_label_kws={}, ax=ax,
                   colors=['blue'])

ax.scatter(max_coords_point[0], max_coords_point[1], color='blue', marker='o', s=30)
# cross section lines
plt.axhline(y=max_coords_point[1], color='blue', linestyle='-.')
plt.axvline(x=max_coords_point[0], color='blue', linestyle=':')

# PATH
raster_path = rasterio.open(file_list[0])
raster_array_path = raster_path.read(1)
# make all 0 vals in array nan
raster_array_path[raster_array_path == 0.0] = np.nan
# force non-zero vals to be 1
bool_arr_path = np.ones(raster_array_path.shape)
# remove nans in bool array
nan_index_path = np.where(np.isnan(raster_array_path))
bool_arr_path[nan_index_path] = 0.0
# get location of max val
ind_max_2d_path = np.unravel_index(np.nanargmax(raster_array_path), raster_array_path.shape)[:]
max_coords_path = raster_path.xy(ind_max_2d_path[0], ind_max_2d_path[1])
# plot
rasterio.plot.show(bool_arr_path, transform=raster_path.transform, contour=True, contour_label_kws={}, ax=ax,
                   colors=['red'])
ax.scatter(max_coords_path[0], max_coords_path[1], color='red', marker='o', s=30)
# cross section lines
plt.axhline(y=max_coords_path[1], color='red', linestyle='-.')
plt.axvline(x=max_coords_path[0], color='red', linestyle=':')

# plot path
df = gpd.read_file(sa_dir + 'fake_path3.shp')
df.plot(edgecolor='red', ax=ax, linewidth=4.0, linestyle='-', label='LAS')
# plot EC
ax.scatter(283940.6056, 5712253.017, color='blue', marker='X', s=100, zorder=10, label='EC')
# ticks
ax.ticklabel_format(style='plain')
plt.legend(loc='upper left')
plt.yticks(rotation=90, va="center")

# plt.savefig(save_path + 'concept_fig_map.png', bbox_inches='tight')

print('end')
