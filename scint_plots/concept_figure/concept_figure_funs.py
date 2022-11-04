import rasterio.plot
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import matplotlib as mpl
import pandas as pd

mpl.rcParams.update({'font.size': 15})  # updating the matplotlib fontsize


def run_concept_fig(save_path):
    """

    :return:
    """

    sa_dir = save_path + 'sa_files_used/'

    # find files
    file_list = find_sa_files(sa_dir)

    # prep for plot
    in_dict = handle_raster(file_list)

    # plot
    plot_concept_axis(in_dict, save_path)


def find_sa_files(sa_dir):
    """

    :return:
    """

    file_list = []
    os.chdir(sa_dir)
    for file in glob.glob("*.tif"):
        file_list.append(sa_dir + file)

    return file_list


def handle_raster(file_list):
    """

    :return:
    """

    # PATH
    raster_path = rasterio.open(file_list[0])
    raster_array_path = raster_path.read(1)

    height_path = raster_array_path.shape[0]
    width_path = raster_array_path.shape[1]
    cols_path, rows_path = np.meshgrid(np.arange(width_path), np.arange(height_path))
    xs_path, ys_path = rasterio.transform.xy(raster_path.transform, rows_path, cols_path)
    lons_path = np.array(xs_path)
    lats_path = np.array(ys_path)

    # make all 0 vals in array nan
    raster_array_path[raster_array_path == 0.0] = np.nan

    # cross sections
    # north to south
    y_crosssec_path = raster_array_path[:, np.where(raster_array_path == np.nanmax(raster_array_path))[1][0]]
    y_crosssec_path_distance = lats_path[:, np.where(raster_array_path == np.nanmax(raster_array_path))[1][0]]
    # east to west
    x_crosssec_path = raster_array_path[np.where(raster_array_path == np.nanmax(raster_array_path))[0][0], :]
    x_crosssec_path_distance = lons_path[np.where(raster_array_path == np.nanmax(raster_array_path))[0][0], :]

    # force integrate to 1
    y_crosssec_to1_path = (1 / np.nansum(y_crosssec_path)) * y_crosssec_path
    x_crosssec_to1_path = (1 / np.nansum(x_crosssec_path)) * x_crosssec_path

    # POINT
    raster_point = rasterio.open(file_list[1])
    raster_array_point = raster_point.read(1)

    height_point = raster_array_point.shape[0]
    width_point = raster_array_point.shape[1]
    cols_point, rows_point = np.meshgrid(np.arange(width_point), np.arange(height_point))
    xs_point, ys_point = rasterio.transform.xy(raster_point.transform, rows_point, cols_point)
    lons_point = np.array(xs_point)
    lats_point = np.array(ys_point)

    # make all 0 vals in array nan
    raster_array_point[raster_array_point == 0.0] = np.nan

    # cross sections
    # north to south
    y_crosssec_point = raster_array_point[:, np.where(raster_array_point == np.nanmax(raster_array_point))[1][0]]
    y_crosssec_point_distance = lats_point[:, np.where(raster_array_point == np.nanmax(raster_array_point))[1][0]]
    # east to west
    x_crosssec_point = raster_array_point[np.where(raster_array_point == np.nanmax(raster_array_point))[0][0], :]
    x_crosssec_point_distance = lons_point[np.where(raster_array_point == np.nanmax(raster_array_point))[0][0], :]

    # force integrate to 1
    y_crosssec_to1_point = (1 / np.nansum(y_crosssec_point)) * y_crosssec_point
    x_crosssec_to1_point = (1 / np.nansum(x_crosssec_point)) * x_crosssec_point

    # OPTIONAL STEP
    # scale all weights to one
    """
    x_crosssec_to1_point = (1 / np.nanmax(x_crosssec_to1_point))*x_crosssec_to1_point
    y_crosssec_to1_point = (1 / np.nanmax(y_crosssec_to1_point))*y_crosssec_to1_point
    x_crosssec_to1_path = (1 / np.nanmax(x_crosssec_to1_path))*x_crosssec_to1_path
    y_crosssec_to1_path = (1 / np.nanmax(y_crosssec_to1_path))*y_crosssec_to1_path
    """

    df_las_lat = pd.DataFrame.from_dict({'lat': x_crosssec_path_distance, 'x_crosssec_to1_path': x_crosssec_to1_path})
    df_las_lat = df_las_lat.set_index('lat')
    df_las_lat = df_las_lat.dropna()
    df_ec_lat = pd.DataFrame.from_dict({'lat': x_crosssec_point_distance, 'x_crosssec_to1_point': x_crosssec_to1_point})
    df_ec_lat = df_ec_lat.set_index('lat')
    df_ec_lat = df_ec_lat.dropna()
    df_las_lon = pd.DataFrame.from_dict({'lon': y_crosssec_path_distance, 'y_crosssec_to1_path': y_crosssec_to1_path})
    df_las_lon = df_las_lon.set_index('lon')
    df_las_lon = df_las_lon.dropna()
    df_ec_lon = pd.DataFrame.from_dict({'lon': y_crosssec_point_distance, 'y_crosssec_to1_point': y_crosssec_to1_point})
    df_ec_lon = df_ec_lon.set_index('lon')
    df_ec_lon = df_ec_lon.dropna()

    # column for meters from minimum lat
    # find minimum lat
    min_lat = min(df_las_lat.index.min(), df_ec_lat.index.min())
    df_las_lat['m_from_min_lat'] = df_las_lat.index - min_lat
    df_ec_lat['m_from_min_lat'] = df_ec_lat.index - min_lat

    # column for meters from minimum lon
    # find minimum lon
    min_lon = min(df_las_lon.index.min(), df_ec_lon.index.min())
    df_las_lon['m_from_min_lon'] = df_las_lon.index - min_lon
    df_ec_lon['m_from_min_lon'] = df_ec_lon.index - min_lon

    # get the same scale in both the lat and lon directions the plot
    # find the max lat and lon
    max_lat = max(df_las_lat.index.max(), df_ec_lat.index.max())
    max_lon = max(df_las_lon.index.max(), df_ec_lon.index.max())

    # make sure that the max and min lat comes from LAS
    assert df_las_lat.index.max() == max_lat
    assert df_las_lat.index.min() == min_lat

    # make sure that the max and min lon comes from LAS
    assert df_las_lon.index.min() == min_lon
    assert df_las_lon.index.max() == max_lon

    # find the difference between max and min lat and lon
    lat_diff = max_lat - min_lat
    lon_diff = max_lon - min_lon

    # find the biggest of these differences between lat and lon
    max_diff = max(lat_diff, lon_diff)

    # get the biggest difference
    if lat_diff == max_diff:
        diff = (lat_diff - lon_diff) / 2
    else:
        diff = (lon_diff - lat_diff) / 2
    assert diff > 0

    # add the difference / 2 to both sides of the smaller direction
    # create temporary df to add a 0 weight to EC and LAS lons
    temp_point_lon = pd.DataFrame.from_dict(
        {'lon': [df_ec_lon.index.max() + diff, df_ec_lon.index.min() - diff], 'y_crosssec_to1_point': [np.nan, np.nan]})
    temp_path_lon = pd.DataFrame.from_dict(
        ({'lon': [df_las_lon.index.max() + diff, df_las_lon.index.min() - diff],
          'y_crosssec_to1_path': [np.nan, np.nan]}))

    temp_point_lon = temp_point_lon.set_index('lon')
    temp_path_lon = temp_path_lon.set_index('lon')

    df_ec_lon_combine = pd.concat([df_ec_lon, temp_point_lon])
    df_las_lon_combine = pd.concat([df_las_lon, temp_path_lon])

    # redefine this
    max_lat = max(df_las_lat.index.max(), df_ec_lat.index.max())
    max_lon = max(df_las_lon_combine.index.max(), df_ec_lon_combine.index.max())
    min_lat = min(df_las_lat.index.min(), df_ec_lat.index.min())
    min_lon = min(df_las_lon_combine.index.min(), df_ec_lon_combine.index.min())

    return {'df_las_lat': df_las_lat,
            'min_lat': min_lat,
            'df_ec_lat': df_ec_lat,
            'df_las_lon': df_las_lon,
            'min_lon': min_lon,
            'df_ec_lon': df_ec_lon,
            'max_lon': max_lon,
            'max_lat': max_lat}


def plot_concept_axis(in_dict, save_path):
    """

    :param in_dict:
    :return:
    """

    df_las_lat = in_dict['df_las_lat']
    min_lat = in_dict['min_lat']
    df_ec_lat = in_dict['df_ec_lat']
    df_las_lon = in_dict['df_las_lon']
    min_lon = in_dict['min_lon']

    df_ec_lon = in_dict['df_ec_lon']
    max_lon = in_dict['max_lon']
    max_lat = in_dict['max_lat']

    fig, ax = plt.subplots(figsize=(15, 3))
    ax2 = ax.twiny()
    # east to west
    las_lat = ax2.plot(df_las_lat.index - min_lat, df_las_lat.x_crosssec_to1_path, label='LAS cross-wind',
                       color='green',
                       linestyle='-')
    ec_lat = ax2.plot(df_ec_lat.index - min_lat, df_ec_lat.x_crosssec_to1_point, label='EC cross-wind', color='green',
                      linestyle='--')
    ax2.set_xlabel('Latitudinal Distance (m)')
    ax2.set_ylabel('SA Weight')

    # north to south
    las_lon = ax.plot(df_las_lon.index - min_lon, df_las_lon.y_crosssec_to1_path, label='LAS along-wind',
                      color='magenta',
                      linestyle='-')
    ec_lon = ax.plot(df_ec_lon.index - min_lon, df_ec_lon.y_crosssec_to1_point, label='EC along-wind', color='magenta',
                     linestyle='--')
    ax.set_xlabel('Longitudinal Distance (m)')
    ax.ticklabel_format(style='plain')
    lns = las_lat + las_lon + ec_lat + ec_lon
    labs = [l.get_label() for l in lns]

    # ax.legend(lns, labs, loc='upper left', prop={'size': 10})
    leg = ax.legend(lns, labs, loc='center left', bbox_to_anchor=(1, 0.5), title="Cross Sections",
                    labelcolor='linecolor')

    plt.gca().set_ylim(bottom=0)

    # colour
    ax2.spines['top'].set_color('green')
    ax2.tick_params(axis='x', colors='green')
    ax2.xaxis.label.set_color('green')
    ax2.spines['bottom'].set_color('magenta')
    ax.tick_params(axis='x', colors='magenta')
    ax.xaxis.label.set_color('magenta')

    # CHANGE HERE
    ax.set_ylabel('SA Weight')
    # OR
    # ax.set_ylabel('% of max SA Weight')
    # ax.set_ylim(0,1)

    ax.set_xlim(0, max_lon - min_lon)
    ax2.set_xlim(0, max_lat - min_lat)

    plt.savefig(save_path + 'fake_path_transect_Vertical' + '.png', bbox_inches='tight', dpi=500)
    print('end')
