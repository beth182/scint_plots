import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

mpl.rcParams.update({'font.size': 15})

from model_eval_tools.retrieve_UKV import find_model_files
from model_eval_tools import look_up
from model_eval_tools.retrieve_UKV import read_premade_model_files
from model_eval_tools.retrieve_UKV import retrieve_ukv_vars_tools


def model_data_at_heights(DOY,
                          obs_df,
                          grid_number=13):
    """

    :return:
    """

    # get model DOY
    DOY_model = retrieve_ukv_vars_tools.UKV_return_model_DOY(DOY, DOY, '21Z')['DOYstart_mod']
    DOYstop_mod = retrieve_ukv_vars_tools.UKV_return_model_DOY(DOY, DOY, '21Z')['DOYstop_mod']

    # can only handle 1 day at a time atm
    assert DOY_model == DOYstop_mod

    # get filepaths
    retrieve_model_filepath_BL_H_dict = retrieve_model_filepath(DOY_model, 'BL_H', grid_number=grid_number)
    retrieve_model_filepath_H_dict = retrieve_model_filepath(DOY_model, 'H', grid_number=grid_number)

    BL_H_path = retrieve_model_filepath_BL_H_dict['model_file_path']
    H_path = retrieve_model_filepath_H_dict['model_file_path']

    # get site string
    site_string = retrieve_model_filepath_BL_H_dict['site_string']
    H_site = retrieve_model_filepath_H_dict['site_string']

    # get grid choice
    grid_choice = retrieve_model_filepath_BL_H_dict['grid_choice']
    H_grid_choice = retrieve_model_filepath_H_dict['grid_choice']

    # make sure file source is the same for both surface and level files
    assert site_string == H_site
    assert grid_choice == H_grid_choice

    # read in nc files
    BL_H_ncfile = nc.Dataset(BL_H_path)
    H_ncfile = nc.Dataset(H_path)

    # model time
    time_dict_returns_BL_H = read_premade_model_files.handle_model_time(BL_H_ncfile, BL_H_path, site_string)
    index_to_start = time_dict_returns_BL_H['index_to_start']
    model_time = time_dict_returns_BL_H['model_time']

    time_dict_returns_H = read_premade_model_files.handle_model_time(H_ncfile, H_path, site_string)
    index_to_start_H = time_dict_returns_H['index_to_start']
    model_time_H = time_dict_returns_H['model_time']

    assert index_to_start_H == index_to_start
    assert model_time == model_time_H

    # model levels
    model_heights = BL_H_ncfile.variables['level_height'][:]

    # grid choices
    grid_choice_dict = read_premade_model_files.grid_choice_indexes(grid_choice)
    index_lat = grid_choice_dict['index_lat']
    index_lon = grid_choice_dict['index_lon']

    # read in variables
    var = BL_H_ncfile.variables['boundary_layer_heat_fluxes']
    var_surf = H_ncfile.variables['surface_sensible_heat_flux']

    # grid_latitude, grid_longitude, time, model_level_number
    var_grid = var[index_lat, index_lon, index_to_start:index_to_start + 24, :]
    var_surf_grid = var_surf[index_lat, index_lon, index_to_start:index_to_start + 24]

    # create plot
    create_model_height_plot(model_time, var_grid, var_surf_grid, model_heights, obs_df)


def retrieve_model_filepath(DOY,
                            variable,
                            grid_number=13):
    """
    Returns model file path as just a string
    :return:
    """
    # ToDo: does this belong here?
    # ToDo: does this have other utility?

    # determine model site
    site_options = look_up.grid_dict[grid_number]
    site_string = site_options[0].split(' ')[0]

    grid_choice = site_options[0].split(' ')[1]

    # find model file
    model_file_dict = find_model_files.find_UKV_files(DOY,
                                                      DOY,
                                                      site_string,
                                                      'ukv',
                                                      '21Z',
                                                      variable,
                                                      model_path="//rdg-home.ad.rdg.ac.uk/research-nfs/basic/micromet/Tier_processing/rv006011/new_data_storage/"
                                                      )

    # sort stash codes
    files_ukv = find_model_files.order_model_stashes(model_file_dict, variable)

    # untangle just the string for the file path
    model_file_path = [(k, v) for k, v in files_ukv.items()][0][1]

    return {'model_file_path': model_file_path, 'grid_choice': grid_choice, 'site_string': site_string}


def create_model_height_plot(model_times,
                             var_grid,
                             var_surf_grid,
                             model_heights,
                             obs_df):
    """
    Plotting function
    :return:
    """

    # colours
    cmap = plt.cm.rainbow  # define the colormap
    # extract all colors from the .jet map
    cmaplist = [cmap(i) for i in range(cmap.N)]

    list_len = len(model_times)

    colour_len = len(cmaplist)

    colour_intervals = int(colour_len / list_len)

    colour_list = []

    count = 0
    for i in model_times:
        color_choice = cmaplist[count]
        colour_list.append(color_choice)
        count += colour_intervals

    fig, ax = plt.subplots(figsize=(10, 10))

    for i in range(len(model_times)):
        qh_at_1_time = var_grid[i, :]
        plt.plot(qh_at_1_time, model_heights, label=str(i), color=colour_list[i], marker='o', linestyle='dotted')
        plt.scatter(var_surf_grid[i], 0, color=colour_list[i], marker='x')

    # get range of observation effective measurement height
    max_z_f = np.nanmax(obs_df)
    min_z_f = np.nanmin(obs_df)
    plt.axhspan(min_z_f, max_z_f, alpha=0.2, color='red')

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={'size': 15})

    plt.ylim(-2, 150)
    plt.xlim(-50, max(var_surf_grid) + 10)
    plt.ylabel("Height above $z_{ES}$ (m)")
    plt.xlabel('$Q_{H}$ (W m$^{-2}$)')

    # manually set the first x tick
    # We need to draw the canvas, otherwise the labels won't be positioned and won't have values yet.
    fig.canvas.draw()

    labels = [item.get_text() for item in ax.get_yticklabels()]
    labels[1] = '$z_{ES}$'

    ax.set_yticklabels(labels)

    # set title
    if obs_df.index[0].strftime('%j') == '126':
        title_string = 'Clear'
    else:
        assert obs_df.index[0].strftime('%j') == '123'
        title_string = 'Cloudy'
    plt.title(title_string)

    plt.tight_layout()

    # save plot
    plt.savefig('./' + obs_df.index[0].strftime('%Y%j') + '_model_levels.png', bbox_inches='tight', dpi=300)
    print('Saved here:' + './' + obs_df.index[0].strftime('%Y%j') + '_model_levels.png')
    print('end')
