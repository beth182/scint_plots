import rasterio.plot
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import geopandas as gpd
import matplotlib.colors as colors
import matplotlib as mpl

mpl.rcParams.update({'font.size': 15})


def find_SA_rasters(sa_main_dir='C:/Users/beths/Desktop/LANDING/combine_rasters/',
                    given_list=False,
                    **kwargs):
    """

    :param given_list:
    :param sa_file_source:
    :return:
    """
    if given_list:
        sa_file_source = kwargs['sa_file_source']

        list_of_files = []
        for sa_name in sa_file_source:
            new_path = sa_main_dir + sa_name
            list_of_files.append(new_path)

    else:

        # deal with files
        list_of_files = []
        os.chdir(sa_main_dir)
        for file in glob.glob("*.tif"):
            list_of_files.append(sa_main_dir + file)

    return list_of_files


def get_colours(cmap, file_list):
    """

    :param cmap:
    :param file_list:
    :return:
    """
    # extract all colors from the map
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

    return colour_list


def plot_sa_lines(file_list,
                  colour_list,
                  doy_choice,
                  save_path,
                  landcover_raster_filepath='C:/Users/beths/OneDrive - University of Reading/Model_Eval/QGIS/Elliott/LandUseMM_7classes_32631.tif'):
    """

    :return:
    """

    fig, ax = plt.subplots(figsize=(10, 10))

    # plot the land cover map
    landcover_raster = rasterio.open(landcover_raster_filepath)
    color_list_lc = ["white", "dimgrey", "lightgrey", "deepskyblue", "lawngreen", "darkgreen", "limegreen", "olive"]
    # make a color map of fixed colors
    cmap_lc = colors.ListedColormap(color_list_lc)
    bounds_lc = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    norm_lc = colors.BoundaryNorm(bounds_lc, cmap_lc.N)
    rasterio.plot.show(landcover_raster, ax=ax, cmap=cmap_lc, norm=norm_lc, interpolation='nearest', alpha=0.5)

    # plot the SAs
    for i, filename in enumerate(file_list):

        # labels as time
        replc = filename.replace('.', '_')
        splt = replc.split('_')
        labels = splt[-3] + ':' + splt[-2]

        raster = rasterio.open(filename)
        raster_array = raster.read()

        # make all 0 vals in array nan
        raster_array[raster_array == 0.0] = np.nan

        # force non-zero vals to be 1
        bool_arr = np.ones(raster_array.shape)

        # remove nans in bool array
        nan_index = np.where(np.isnan(raster_array))
        bool_arr[nan_index] = 0.0

        # get location of max val
        ind_max_2d = np.unravel_index(np.nanargmax(raster_array), raster_array.shape)[1:]
        max_coords = raster.xy(ind_max_2d[0], ind_max_2d[1])

        # Plot the SA line
        if type(colour_list[i]) == str:
            colour_here = colour_list[i]
        else:
            colour_here = list(colour_list[i])

        ax.scatter(max_coords[0], max_coords[1], color=colour_here, marker='o', s=30, label=labels)

        rasterio.plot.show(bool_arr, transform=raster.transform, contour=True, contour_label_kws={}, ax=ax,
                           colors=[colour_here])

    handles, labels = ax.get_legend_handles_labels()

    plt.legend(handles=handles, loc='upper left')
    plt.yticks(rotation=90)

    # limits which stay constant between and which suit both day's SAs
    ax.set_xlim(279685.28503960633, 289345.4708460579)
    ax.set_ylim(5707118.9139011325, 5716431.904868875)

    # plot paths
    df_12 = gpd.read_file('C:/Users/beths/Desktop/LANDING/scint_path_shp/BCT_IMU.shp')
    df_12.plot(edgecolor='green', ax=ax, linewidth=3.0)

    # title
    if doy_choice == 126:
        title_string = 'Clear'
    else:
        assert doy_choice == 123
        title_string = 'Cloudy'

    plt.title(title_string)

    plt.savefig(save_path + 'sa_lines_' + str(doy_choice) + '.png', bbox_inches='tight', dpi=300)
    print('end')
