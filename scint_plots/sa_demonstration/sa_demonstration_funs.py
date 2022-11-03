import rasterio.plot
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import geopandas as gpd
import matplotlib as mpl
import matplotlib.colors as colors

mpl.rcParams.update({'font.size': 15})


def run_panel_figs(panel_number, save_path):
    """
    Main function to call one of 3 panel plots
    :param panel_number:
    :return:
    """

    if panel_number == 1:
        sa_dir = save_path + 'sa_files_used/point_fp/'
        file_list = collect_obs_sa(sa_dir)
        panel_one(file_list, save_path)
    elif panel_number == 2:
        sa_dir = save_path + 'sa_files_used/'
        sa_file_list = collect_obs_sa(sa_dir)
        ukv_file_list = collect_UKV_grid_shp()
        panel_two(sa_file_list, ukv_file_list, save_path)

    elif panel_number == 3:
        sa_dir = save_path + 'sa_files_used/'
        sa_file_list = collect_obs_sa(sa_dir)
        ukv_file_list = collect_UKV_grid_shp()
        panel_three(sa_file_list, ukv_file_list, save_path)

    else:
        raise ValueError('Only panel numbers 1-3')


def collect_obs_sa(sa_dir):
    """
    Collects observation SAs avail in a directory
    :return:
    """

    file_list = []
    os.chdir(sa_dir)
    for file in glob.glob("*.tif"):
        file_list.append(sa_dir + file)

    return file_list


def collect_UKV_grid_shp(grid_dir='C:/Users/beths/Desktop/LANDING/UKV_shapefiles/'):
    """
    Collects all UKV gridboxes avail into a list
    ToDo: move grid_dir to local
    :return:
    """

    grid_file_list = []
    os.chdir(grid_dir)
    for file in glob.glob("*.shp"):
        grid_file_list.append(grid_dir + file)

    return grid_file_list


def handle_raster(file_path):
    """

    :return:
    """

    raster = rasterio.open(file_path)
    raster_array = raster.read()

    # make all 0 vals in array nan
    raster_array[raster_array == 0.0] = np.nan

    # force non-zero vals to be 1
    bool_arr = np.ones(raster_array.shape)

    # remove nans in bool array
    nan_index = np.where(np.isnan(raster_array))
    bool_arr[nan_index] = 0.0

    return {'raster': raster, 'bool_arr': bool_arr, 'raster_array': raster_array}


def init_map(file_list, panel_number):
    """
    Initialises map plot - so all panels have the same bounds etc.
    :return:
    """

    # read the first raster in the list to get location and plot basemap
    raster0 = rasterio.open(file_list[0])
    fig, ax = plt.subplots(figsize=(12, 12))
    # hide this one with alpha 0
    rasterio.plot.show(raster0, ax=ax, alpha=0.0)

    # plot the land cover map
    # ToDo: move this
    landcover_raster_filepath = 'C:/Users/beths/OneDrive - University of Reading/Model_Eval/QGIS/Elliott/LandUseMM_7classes_32631.tif'
    landcover_raster = rasterio.open(landcover_raster_filepath)
    color_list_lc = ["white", "dimgrey", "lightgrey", "deepskyblue", "lawngreen", "darkgreen", "limegreen", "olive"]
    # make a color map of fixed colors
    cmap_lc = colors.ListedColormap(color_list_lc)
    bounds_lc = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    norm_lc = colors.BoundaryNorm(bounds_lc, cmap_lc.N)
    rasterio.plot.show(landcover_raster, ax=ax, cmap=cmap_lc, norm=norm_lc, interpolation='nearest', alpha=0.3)

    # sex ax lims
    ax.set_xlim(281314.7269919119, 285676.31545750913)
    ax.set_ylim(5709795.207536185, 5713837.796845389)

    plt.yticks(rotation=90)

    if panel_number == 2:
        image_hidden = ax.imshow(raster0.read(1))
        # divider = make_axes_locatable(ax)
        # cax = divider.append_axes("top", size="5%", pad=0.05)
        cax = fig.add_axes([0.27, 0.18, 0.5, 0.02])
        fig.colorbar(image_hidden, ax=ax, cax=cax, orientation='horizontal')

    return fig, ax


def panel_one(file_list, save_path):
    """
    Show individually calculated point footprints
    :param file_list: list of filepaths for individual EC footprints
    :return:
    """

    # colours
    cmap = plt.cm.inferno  # define the colormap
    # extract all colors from the .jet map
    cmaplist = [cmap(i) for i in range(cmap.N)]
    list_len = len(file_list)
    colour_len = len(cmaplist)
    colour_intervals = int(colour_len / list_len)
    colour_list = []
    count = 0
    for i in file_list:
        color_choice = cmaplist[count]
        colour_list.append(color_choice)
        count += colour_intervals

    # init plot
    fig, ax = init_map(file_list, 1)

    # handle raster
    for i, file_path in enumerate(file_list):
        raster_dict = handle_raster(file_path)
        bool_arr = raster_dict['bool_arr']
        raster = raster_dict['raster']

        # plot lines
        colour_here = list(colour_list[i])
        rasterio.plot.show(bool_arr, transform=raster.transform, contour=True, contour_label_kws={}, ax=ax,
                           colors=[colour_here])

    # plot path
    # ToDo: move path shp file
    df = gpd.read_file('C:/Users/beths/Desktop/LANDING/scint_path_shp/BCT_IMU.shp')
    df.plot(edgecolor='green', ax=ax, linewidth=4.0, zorder=1)

    # plot points
    df_points = gpd.read_file(save_path + 'sa_files_used/points/weighted.shp')
    colour_list_cmap = mpl.colors.LinearSegmentedColormap.from_list("", colour_list)
    df_points.plot(ax=ax, cmap=colour_list_cmap, zorder=2, markersize=100, edgecolors='black')

    plt.savefig(save_path + 'panel_1.png', bbox_inches='tight', dpi=300)
    print('end')


def panel_two(sa_file_list,
              ukv_file_list,
              save_path):
    """
    Show a path footprint with colourbar, and UKV grids.
    :param sa_file_list: List (len=1) of filepath of one path footprint raster
    :param ukv_file_list: List of filepaths of UKV gridbox shp files
    :return:
    """

    # init plot
    fig, ax = init_map(sa_file_list, 2)

    # handle raster
    for i, file_path in enumerate(sa_file_list):
        raster_dict = handle_raster(file_path)
        raster = raster_dict['raster']
        raster_array = raster_dict['raster_array']

        # plot SA
        rasterio.plot.show(raster_array, transform=raster.transform, ax=ax)

    # plot path
    # ToDo: move path shp file
    df = gpd.read_file('C:/Users/beths/Desktop/LANDING/scint_path_shp/BCT_IMU.shp')
    df.plot(edgecolor='green', ax=ax, linewidth=4.0, zorder=1)

    # plot equal points
    df_points = gpd.read_file(save_path + 'sa_files_used/points/equal.shp')
    df_points.plot(ax=ax, color='yellow', zorder=2, marker='.', markersize=120, edgecolors='black')

    # plot UKV grid boxes
    for file in ukv_file_list:
        df_grid = gpd.read_file(file)
        df_grid.plot(ax=ax, zorder=0)

    plt.savefig(save_path + 'panel_2.png', bbox_inches='tight', dpi=300)
    print('end')


def panel_three(sa_file_list,
                ukv_file_list,
                save_path):
    """

    :return:
    """

    # init plot
    fig, ax = init_map(sa_file_list, 3)

    # handle raster
    for i, file_path in enumerate(sa_file_list):
        raster_dict = handle_raster(file_path)
        raster = raster_dict['raster']
        bool_arr = raster_dict['bool_arr']

        # plot SA
        colour_here = 'black'
        rasterio.plot.show(bool_arr, transform=raster.transform, contour=True, contour_label_kws={}, ax=ax,
                           colors=[colour_here])

    # plot path
    # ToDo: move path shp file
    df = gpd.read_file('C:/Users/beths/Desktop/LANDING/scint_path_shp/BCT_IMU.shp')
    df.plot(edgecolor='green', ax=ax, linewidth=4.0, zorder=1)

    # plot UKV grid boxes
    for file in ukv_file_list:
        df_grid = gpd.read_file(file)
        df_grid.plot(ax=ax)

    plt.savefig(save_path + 'panel_3.png', bbox_inches='tight', dpi=300)
    print('end')
