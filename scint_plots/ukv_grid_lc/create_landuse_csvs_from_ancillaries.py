# Moving this code over from legacy Model eval
# This is all garbage and needs to be addressed if used again
# the saved output is what is used and this shouldn't need to be run again

import csv
import iris
import cartopy.crs as ccrs
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys

mpl.rcParams.update({'font.size': 20})  # updating the matplotlib fontsize

# lat and lon of old file format 3x3 grids
nine_grids = {
    'BTT': [[[51.51391602, 51.51348114, 51.51304626],
             [51.5274086, 51.52697372, 51.52653503],
             [51.54090118, 51.54046631, 51.54002762]],
            [[359.82943726, 359.85092163, 359.87249756],
             [359.83001709, 359.85159302, 359.87322998],
             [359.83078003, 359.85244751, 359.87387085]]],

    'BCT':
        [[[51.51259232, 51.51214981, 51.51169586],
          [51.5260849, 51.52563858, 51.52518463],
          [51.5395813, 51.53913116, 51.53867722]],
         [[359.89440918, 359.915802, 359.93743896],
          [359.89498901, 359.91653442, 359.93823242],
          [359.89581299, 359.9173584, 359.93911743]]],

    'BFCL':
        [[[51.51259232, 51.51214981, 51.51169586],
          [51.5260849, 51.52563858, 51.52518463],
          [51.5395813, 51.53913116, 51.53867722]],
         [[359.89440918, 359.915802, 359.93743896],
          [359.89498901, 359.91653442, 359.93823242],
          [359.89581299, 359.9173584, 359.93911743]]],

    'BGH':
        [[[51.49909973, 51.49865723, 51.49820328],
          [51.51259232, 51.51214981, 51.51169586],
          [51.5260849, 51.52563858, 51.52518463]],
         [[359.89367676, 359.91525269, 359.93685913],
          [359.89440918, 359.915802, 359.93743896],
          [359.89498901, 359.91653442, 359.93823242]]],

    'IML':
        [[[51.51304626, 51.51259232, 51.51214981],
          [51.52653503, 51.5260849, 51.52563858],
          [51.54002762, 51.5395813, 51.53913116]],
         [[359.87249756, 359.89440918, 359.915802],
          [359.87322998, 359.89498901, 359.91653442],
          [359.87387085, 359.89581299, 359.9173584]]],

    'IMU':
        [[[51.51304626, 51.51259232, 51.51214981],
          [51.52653503, 51.5260849, 51.52563858],
          [51.54002762, 51.5395813, 51.53913116]],
         [[359.87249756, 359.89440918, 359.915802],
          [359.87322998, 359.89498901, 359.91653442],
          [359.87387085, 359.89581299, 359.9173584]]],

    'MR':
        [[[51.51391602, 51.51348114, 51.51304626],
          [51.5274086, 51.52697372, 51.52653503],
          [51.54090118, 51.54046631, 51.54002762]],
         [[359.82943726, 359.85092163, 359.87249756],
          [359.83001709, 359.85159302, 359.87322998],
          [359.83078003, 359.85244751, 359.87387085]]],

    'NK':
        [[[51.5017128, 51.50128937, 51.50086212],
          [51.51520538, 51.51478195, 51.51435471],
          [51.52869797, 51.52827454, 51.52784729]],
         [[359.7635498, 359.7850647, 359.80673218],
          [359.76434326, 359.78585815, 359.80764771],
          [359.76495361, 359.78643799, 359.80807495]]],

    'RGS':
        [[[51.48736954, 51.48693085, 51.48649979],
          [51.50086212, 51.50042725, 51.49999237],
          [51.51435471, 51.51391602, 51.51348114]],
         [[359.80612183, 359.82809448, 359.84936523],
          [359.80673218, 359.82861328, 359.85018921],
          [359.80764771, 359.82943726, 359.85092163]]],

    'KSSW':
        [[[51.49955368, 51.49909973, 51.49865723],
          [51.51304626, 51.51259232, 51.51214981],
          [51.52653503, 51.5260849, 51.52563858]],
         [[359.87191772, 359.89367676, 359.91525269],
          [359.87249756, 359.89440918, 359.915802],
          [359.87322998, 359.89498901, 359.91653442]]],

    'SWT':
        [[[51.47212334, 51.47167429, 51.47122121],
          [51.48561591, 51.48516673, 51.4847135],
          [51.49910847, 51.49865916, 51.49820579]],
         [[359.89209097, 359.91374853, 359.93540566],
          [359.89280894, 359.91447299, 359.93613661],
          [359.89352734, 359.91519788, 359.93686799]]],

    'SWINDON':
        [[[51.5846, 51.5846, 51.5846],
          [51.5846, 51.5846, 51.5846],
          [51.5846, 51.5846, 51.5846]],
         [[358.2019, 358.2019, 358.2019],
          [358.2019, 358.2019, 358.2019],
          [358.2019, 358.2019, 358.2019]]]}


def get_landuse_fraction9(site,
                          landuse,
                          grid_letter,
                          frac_file_location):
    """
    LEGACY - SHOULD ONLY USE 10 TILE
    gets the fractions of land use -- for the 9-tile file.
    Produces a fraction of land use from 9 tiles: Can give all tiles or a specified tile.

    :param site: site choice as a string.
    :param landuse: Name of the tile which you want the land use for, as a string. Can be:
    broadleaf, needleleaf, C3, C4, shrubs, urban, lake, soil, ice or all for a list of all in <- that order.
    :return: fraction of land use requested. int if 1 type, list if all types.
    """

    # index of land use choices:
    if landuse == 'broadleaf':
        landuse_index = 0
    elif landuse == 'needleleaf':
        landuse_index = 1
    elif landuse == 'C3':
        landuse_index = 2
    elif landuse == 'C4':
        landuse_index = 3
    elif landuse == 'shrubs':
        landuse_index = 4
    elif landuse == 'urban':
        landuse_index = 5
    elif landuse == 'lake':
        landuse_index = 6
    elif landuse == 'soil':
        landuse_index = 7
    elif landuse == 'ice':
        landuse_index = 8
    elif landuse == 'all':
        pass
    else:
        raise ValueError(
            'The landuse option chosen does not exist. Choose again from: broadleaf, needleleaf, C3, C4, shrubs, urban, lake, soil, ice or all')

    # choices based on grid chosen
    if grid_letter == 'A':
        grid = 'grid_7'
    elif grid_letter == 'B':
        grid = 'grid_8'
    elif grid_letter == 'C':
        grid = 'grid_9'
    elif grid_letter == 'D':
        grid = 'grid_4'
    elif grid_letter == 'E':
        grid = 'grid_5'
    elif grid_letter == 'F':
        grid = 'grid_6'
    elif grid_letter == 'G':
        grid = 'grid_1'
    elif grid_letter == 'H':
        grid = 'grid_2'
    elif grid_letter == 'I':
        grid = 'grid_3'
    else:
        raise ValueError('grid choice is not an option.')

    lat_index = 0
    lon_index = 1

    if grid == 'grid_1':
        row = 0
        column = 0
    elif grid == 'grid_2':
        row = 0
        column = 1
    elif grid == 'grid_3':
        row = 0
        column = 2
    elif grid == 'grid_4':
        row = 1
        column = 0
    elif grid == 'grid_5':
        row = 1
        column = 1
    elif grid == 'grid_6':
        row = 1
        column = 2
    elif grid == 'grid_7':
        row = 2
        column = 0
    elif grid == 'grid_8':
        row = 2
        column = 1
    elif grid == 'grid_9':
        row = 2
        column = 2
    else:
        raise ValueError('grid choice not an option.')

    # imports the lon and lat in WGS84 from the variables.py dictionary. format [lon, lat].
    # loc = site_location[site]
    loc = (nine_grids[site][lon_index][row][column], nine_grids[site][lat_index][row][column])
    # X = LON, Y = LAT
    x_old = loc[0]  # lon
    y_old = loc[1]  # lat

    # PATH TO .FRAC FILE

    # one sylvia gave me
    # frac_file_location = '/storage/basic/micromet/Tier_processing/rv006011/landuse/9tile_urban_landuse/qrparm.veg.frac'

    # ps41 9-tile (from Maggie 20180710)
    # frac_file_location = '/storage/basic/micromet/Tier_processing/rv006011/landuse/10tile_moruses_canyon_roof_landuse/maggie_20180710/qrparm.veg.v1.frac'

    # LOAD AS A CUBE
    cube = iris.load_cube(frac_file_location)

    """
    # PLOTS TOTAL UK CUBE
    if landuse == 'all':
        landuse_list = ['broadleaf', 'needleleaf', 'C3', 'C4', 'shrubs', 'urban', 'lake', 'soil', 'ice']
        count = 0
        for item in landuse_list:
            plt.figure(figsize = (10, 20))
            qplt.pcolormesh(cube[count, :, :], vmin=0, vmax=1, cmap='jet')
            plt.gca().coastlines()
            plt.title(item)
            plt.savefig('../plots/landuse_plots/' + 'whole_uk_' + item + '.png', dpi = 200, bbox_inches='tight')
            count += 1
    else:
        plt.figure(figsize = (10, 20))
        qplt.pcolormesh(cube[landuse_index, :, :], vmin=0, vmax=1, cmap='jet')
        plt.gca().coastlines()
        plt.title(landuse)
        plt.savefig('../../plots/landuse_plots/' + 'whole_uk_' + landuse + '.png', dpi = 200, bbox_inches='tight')
    """

    # Then load the land-use into a cube:
    # rotate obs for 55m domains
    # ROTATES THE SITE OLD X AND Y INTO MO WORLD CONVENTION
    rot_pole1 = cube.coord('grid_latitude').coord_system.as_cartopy_crs()
    ll = ccrs.Geodetic()
    target_xy1 = rot_pole1.transform_point(x_old, y_old, ll)  # lower left corner
    x_new = target_xy1[0] + 360.
    y_new = target_xy1[1]

    # FINDS THE CLOSEST COORDINATES TO THE NEW X & Y IN THE MO FILE
    latitudes = cube.coord('grid_latitude')
    longitudes = cube.coord('grid_longitude')
    nearest_lat = latitudes.nearest_neighbour_index(y_new)
    nearest_lon = longitudes.nearest_neighbour_index(x_new)

    # CONSTRAINT
    # EXTRACTS INTEGERS FROM THE NEAREST VALUES FOR THE CONSTRAINT:
    lat_value = latitudes.cell(nearest_lat)
    lon_value = longitudes.cell(nearest_lon)
    gcon = iris.Constraint(coord_values={'grid_latitude': lat_value,
                                         'grid_longitude': lon_value})
    extracted = cube.extract(gcon)

    if landuse == 'all':
        return extracted.data
    else:
        return extracted.data[landuse_index]


# for the 10-tile file...
def get_landuse_fraction10(site,
                           landuse,
                           grid_letter,
                           frac_file_location):
    """
    gets the fractions of land use -- for the 10-tile file.
    Produces a fraction of land use from 10 tiles: Can give all tiles or a specified tile.

    :param site: site choice as a string.
    :param landuse: Name of the tile which you want the land use for, as a string. Can be:
    broadleaf, needleleaf, C3, C4, shrubs, lake, soil, ice, canyon, roof or all for a list of all in <- that order.
    :return: fraction of land use requested. int if 1 type, list if all types.
    """

    # index of land use choices:
    if landuse == 'broadleaf':
        landuse_index = 0
    elif landuse == 'needleleaf':
        landuse_index = 1
    elif landuse == 'C3':
        landuse_index = 2
    elif landuse == 'C4':
        landuse_index = 3
    elif landuse == 'shrubs':
        landuse_index = 4
    elif landuse == 'lake':
        landuse_index = 5
    elif landuse == 'soil':
        landuse_index = 6
    elif landuse == 'ice':
        landuse_index = 7
    elif landuse == 'canyon':
        landuse_index = 8
    elif landuse == 'roof':
        landuse_index = 9
    elif landuse == 'all':
        pass
    else:
        raise ValueError(
            'The landuse option chosen does not exist. Choose again from: broadleaf, needleleaf, C3, C4, shrubs, lake, soil, ice, canyon, roof or all')

    # choices based on grid chosen
    if grid_letter == 'A':
        grid = 'grid_7'
    elif grid_letter == 'B':
        grid = 'grid_8'
    elif grid_letter == 'C':
        grid = 'grid_9'
    elif grid_letter == 'D':
        grid = 'grid_4'
    elif grid_letter == 'E':
        grid = 'grid_5'
    elif grid_letter == 'F':
        grid = 'grid_6'
    elif grid_letter == 'G':
        grid = 'grid_1'
    elif grid_letter == 'H':
        grid = 'grid_2'
    elif grid_letter == 'I':
        grid = 'grid_3'
    else:
        raise ValueError('grid choice is not an option.')

    lat_index = 0
    lon_index = 1

    if grid == 'grid_1':
        row = 0
        column = 0
    elif grid == 'grid_2':
        row = 0
        column = 1
    elif grid == 'grid_3':
        row = 0
        column = 2
    elif grid == 'grid_4':
        row = 1
        column = 0
    elif grid == 'grid_5':
        row = 1
        column = 1
    elif grid == 'grid_6':
        row = 1
        column = 2
    elif grid == 'grid_7':
        row = 2
        column = 0
    elif grid == 'grid_8':
        row = 2
        column = 1
    elif grid == 'grid_9':
        row = 2
        column = 2
    else:
        raise ValueError('grid choice not an option.')

    # imports the lon and lat in WGS84 from the variables.py dictionary. format [lon, lat].
    # loc = site_location[site]
    loc = (nine_grids[site][lon_index][row][column], nine_grids[site][lat_index][row][column])
    # X = LON, Y = LAT
    x_old = loc[0]  # lon
    y_old = loc[1]  # lat

    # PATH TO .FRAC FILE

    # ps41 10-tile (from Maggie 20180710)
    # frac_file_location = '/storage/basic/micromet/Tier_processing/rv006011/landuse/10tile_moruses_canyon_roof_landuse/maggie_20180710/qrparm.veg.frac'

    # LOAD AS A CUBE
    cube = iris.load(frac_file_location)

    """
    # PLOTS TOTAL UK CUBE
    if landuse == 'all':
        landuse_list = ['broadleaf', 'needleleaf', 'C3', 'C4', 'shrubs', 'lake', 'soil', 'ice', 'canyon', 'roof']
        count = 0
        for item in landuse_list:
            plt.figure(figsize=(10, 20))
            qplt.pcolormesh(cube[0][count, :, :], vmin=0, vmax=1, cmap='jet')
            plt.gca().coastlines()
            plt.title(item)
            plt.savefig('../plots/landuse_plots/' + 'whole_uk_' + item + '_10.png', dpi=200, bbox_inches='tight')
            count += 1
    else:
        plt.figure(figsize=(10, 20))
        qplt.pcolormesh(cube[landuse_index, :, :], vmin=0, vmax=1, cmap='jet')
        plt.gca().coastlines()
        plt.title(landuse)
        plt.savefig('../../plots/landuse_plots/' + 'whole_uk_' + landuse + '_10.png', dpi=200, bbox_inches='tight')
    """

    # Then load the land-use into a cube:
    # rotate obs for 55m domains
    # ROTATES THE SITE OLD X AND Y INTO MO WORLD CONVENTION
    rot_pole1 = cube[0].coord('grid_latitude').coord_system.as_cartopy_crs()
    ll = ccrs.Geodetic()
    target_xy1 = rot_pole1.transform_point(x_old, y_old, ll)  # lower left corner
    x_new = target_xy1[0] + 360.
    y_new = target_xy1[1]

    # FINDS THE CLOSEST COORDINATES TO THE NEW X & Y IN THE MO FILE
    latitudes = cube[0].coord('grid_latitude')
    longitudes = cube[0].coord('grid_longitude')
    nearest_lat = latitudes.nearest_neighbour_index(y_new)
    nearest_lon = longitudes.nearest_neighbour_index(x_new)

    # CONSTRAINT
    # EXTRACTS INTEGERS FROM THE NEAREST VALUES FOR THE CONSTRAINT:
    lat_value = latitudes.cell(nearest_lat)
    lon_value = longitudes.cell(nearest_lon)
    gcon = iris.Constraint(coord_values={'grid_latitude': lat_value,
                                         'grid_longitude': lon_value})
    extracted = cube[0].extract(gcon)

    if landuse == 'all':
        return extracted.data
    else:
        return extracted.data[landuse_index]


# for the 10-tile file morphology...
def get_morph_10(site,
                 grid_letter,
                 frac_file_location,
                 stash):
    """
    """

    # choices based on stash chosen
    # URBAN BUILDING HEIGHT
    if stash == 'm01s00i494':
        stash_index = 0
    # URBAN HEIGHT TO WIDTH RATIO
    elif stash == 'm01s00i495':
        stash_index = 1
    # URBAN WIDTH RATIO
    elif stash == 'm01s00i496':
        stash_index = 2
    else:
        raise ValueError('stash code is not an option.')

    # choices based on grid chosen
    if grid_letter == 'A':
        grid = 'grid_7'
    elif grid_letter == 'B':
        grid = 'grid_8'
    elif grid_letter == 'C':
        grid = 'grid_9'
    elif grid_letter == 'D':
        grid = 'grid_4'
    elif grid_letter == 'E':
        grid = 'grid_5'
    elif grid_letter == 'F':
        grid = 'grid_6'
    elif grid_letter == 'G':
        grid = 'grid_1'
    elif grid_letter == 'H':
        grid = 'grid_2'
    elif grid_letter == 'I':
        grid = 'grid_3'
    else:
        raise ValueError('grid choice is not an option.')

    lat_index = 0
    lon_index = 1

    if grid == 'grid_1':
        row = 0
        column = 0
    elif grid == 'grid_2':
        row = 0
        column = 1
    elif grid == 'grid_3':
        row = 0
        column = 2
    elif grid == 'grid_4':
        row = 1
        column = 0
    elif grid == 'grid_5':
        row = 1
        column = 1
    elif grid == 'grid_6':
        row = 1
        column = 2
    elif grid == 'grid_7':
        row = 2
        column = 0
    elif grid == 'grid_8':
        row = 2
        column = 1
    elif grid == 'grid_9':
        row = 2
        column = 2
    else:
        raise ValueError('grid choice is not an option.')

    # imports the lon and lat in WGS84 from the variables.py dictionary. format [lon, lat].
    # loc = site_location[site]
    loc = (nine_grids[site][lon_index][row][column], nine_grids[site][lat_index][row][column])
    # X = LON, Y = LAT
    x_old = loc[0]  # lon
    y_old = loc[1]  # lat

    # LOAD AS A CUBE
    cube = iris.load(frac_file_location)

    # Then load the land-use into a cube:
    # rotate obs for 55m domains
    # ROTATES THE SITE OLD X AND Y INTO MO WORLD CONVENTION
    rot_pole1 = cube[0].coord('grid_latitude').coord_system.as_cartopy_crs()
    ll = ccrs.Geodetic()
    target_xy1 = rot_pole1.transform_point(x_old, y_old, ll)  # lower left corner
    x_new = target_xy1[0] + 360.
    y_new = target_xy1[1]

    # FINDS THE CLOSEST COORDINATES TO THE NEW X & Y IN THE MO FILE
    latitudes = cube[0].coord('grid_latitude')
    longitudes = cube[0].coord('grid_longitude')
    nearest_lat = latitudes.nearest_neighbour_index(y_new)
    nearest_lon = longitudes.nearest_neighbour_index(x_new)

    # CONSTRAINT
    # EXTRACTS INTEGERS FROM THE NEAREST VALUES FOR THE CONSTRAINT:
    lat_value = latitudes.cell(nearest_lat)
    lon_value = longitudes.cell(nearest_lon)
    gcon = iris.Constraint(coord_values={'grid_latitude': lat_value,
                                         'grid_longitude': lon_value})

    extracted = cube[stash_index].extract(gcon)

    return extracted.data


def moruses_param(furb):
    """
    Function to manually calculate the urban roof/ canyon split from Denise.
    MORUSES parameters (wrr,hgt,hwr) from land-use fraction
    Bohnenstengel et al. 2011;  equations copied from MORUSES code by Sylvia

    :param furb: Fraction of urban land use from the 9-tile.
    :return canyon: canyon fraction
    :return roof: roof fraction
    """
    # building plan area fraction
    lambdap = 22.878 * furb ** 6 - 59.473 * furb ** 5 + 57.749 * furb ** 4 - 25.108 * furb ** 3 + 4.3337 * furb ** 2 + 0.1926 * furb + 0.036

    # frontal area index
    lambdaf = 16.412 * furb ** 6 - 41.855 * furb ** 5 + 40.387 * furb ** 4 - 17.759 * furb ** 3 + 3.2399 * furb ** 2 + 0.0626 * furb + 0.0271

    # mean building height
    hgt = 167.409 * furb ** 5 - 337.853 * furb ** 4 + 247.813 * furb ** 3 - 76.3678 * furb ** 2 + 11.4832 * furb + 4.48226

    # height/ street canyon width ratio
    hwr = np.pi / 2.0 * lambdaf / (1.0 - lambdap)

    # wrr = W/R, W = street width, R = total with of street + canyon
    wrr = 1.0 - lambdap

    # canyon fraction
    canyon = wrr * furb
    roof = furb - canyon

    return canyon, roof


def land_use_grids(A, B, C, D, E, F, G, H, I, sitechoice, tile_choice):
    """
    :param A:
    :param B:
    :param C:
    :param D:
    :param E:
    :param F:
    :param G:
    :param H:
    :param I:
    :param sitechoice:
    :param tile_choice: Choice between 9-tile or 10-tile.
    for 9-tile, tile_choice = 9
    for 10-tile, tile_choice = 10
    :return:
    """

    # sets up dataframes
    Adf = pd.DataFrame(
        {'A': A})
    Bdf = pd.DataFrame(
        {'B': B})
    Cdf = pd.DataFrame(
        {'C': C})
    Ddf = pd.DataFrame(
        {'D': D})
    Edf = pd.DataFrame(
        {'E': E})
    Fdf = pd.DataFrame(
        {'F': F})
    Gdf = pd.DataFrame(
        {'G': G})
    Hdf = pd.DataFrame(
        {'H': H})
    Idf = pd.DataFrame(
        {'I': I})
    df_list = [Adf, Bdf, Cdf, Ddf, Edf, Fdf, Gdf, Hdf, Idf]

    # choices based on 9 tile or 10 tile
    if tile_choice == 9:
        series_labels = ['broadleaf tree', 'needleleaf tree', 'C3 grass', 'C4 grass', 'shrubs', 'urban', 'lake', 'soil', 'ice']
        colors = ['teal', 'darkgreen', 'lawngreen', 'coral', 'olive', 'dimgrey', 'deepskyblue', 'sienna', 'lightsteelblue']
        save_string = './plots/landuse_plots/' + sitechoice + '_landuse_grid_9.png'
    elif tile_choice == 10:
        series_labels = ['broadleaf tree', 'needleleaf tree', 'C3 grass', 'C4 grass', 'shrubs', 'lake', 'soil', 'ice', 'canyon', 'roof']
        colors = ['teal', 'darkgreen', 'lawngreen', 'coral', 'olive', 'deepskyblue', 'sienna', 'lightsteelblue', 'dimgrey', 'silver']
        save_string = './plots/landuse_plots/' + sitechoice + '_landuse_grid_10.png'
    else:
        raise ValueError('tile_choice not an option.')

    # plots
    f, ax = plt.subplots(3, 3, figsize=(10, 10))
    ax_list = [ax[0, 0], ax[0, 1], ax[0, 2], ax[1, 0], ax[1, 1], ax[1, 2], ax[2, 0], ax[2, 1], ax[2, 2]]

    for a in range(0, len(df_list)):
        data = list(df_list[a].values)
        ny = len(data[0])
        data = np.array(data)

        ind = list(range(ny))
        axes = []
        cum_size = np.zeros(ny)

        for i, row_data in enumerate(data):
            axes.append(ax_list[a].bar(ind, row_data, bottom=cum_size, color=colors[i], width = 1.0,
                               label=series_labels[i]))
            cum_size += row_data

        if ax_list[a] == ax[0, 0]:
            ax_list[a].axes.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], minor=False)
        elif ax_list[a] == ax[1, 0] or ax_list[a] == ax[2, 0]:
            ax_list[a].axes.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8], minor=False)
        else:
            ax_list[a].axes.get_yaxis().set_visible(False)

        ax_list[a].axes.get_xaxis().set_visible(False)

        xbuffer = 0
        ax_list[a].set_xlim(-xbuffer, len(ind) - 1 + xbuffer)

        ax_list[a].set_ylim(0, 1)

        # gets rid of the axis for the botch put it on the map plot
        # ax_list[a].axes.get_yaxis().set_visible(False)
        plt.legend(bbox_to_anchor=(1.0, 0.5))
        ax[0, 1].set_title(sitechoice)

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.000001, hspace=0.00001)

    plt.savefig(save_string, transparent = True, bbox_inches = 'tight', pad_inches = 0)
    # plt.show()




# USE FOR LANDCOVER
# """
grids = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

sitechoice = ['BFCL', 'BCT', 'IML', 'IMU', 'BGH', 'BTT', 'NK', 'RGS', 'KSSW', 'MR', 'SWT']
# sitechoice = ['KSSW']
# sitechoice = ['IMU']
# sitechoice = ['SWINDON']

# 9-tile Sylvia
# file_location = '/storage/basic/micromet/Tier_processing/rv006011/landuse/sylvia/9tile_urban_landuse/qrparm.veg.frac'
# tile_choice = 9

# 10-tile Sylvia
# DOESN'T WORK
# file_location = 'rv006011/landuse/sylvia/10tile_moruses_canyon_roof_landuse/qrparm.veg.frac'
# tile_choice = 10

# 9-tile Maggie old
# file_location = '/storage/basic/micromet/Tier_processing/rv006011/landuse/maggie_old/qrparm.veg.v1.frac'
# tile_choice = 9

# 10-tile Maggie old
# file_location = '/storage/basic/micromet/Tier_processing/rv006011/landuse/maggie_old/qrparm.veg.frac'
# tile_choice = 10

# 10-tile Maggie new
file_location = '/storage/basic/micromet/Tier_processing/rv006011/landuse/maggie_new/qrparm.veg.frac'
tile_choice = 10


if tile_choice == 9:
    types = ['GRID', 'broadleaf', 'needleleaf', 'C3', 'C4', 'shrubs', 'urban', 'lake', 'soil', 'ice']
elif tile_choice == 10:
    types = ['GRID', 'broadleaf', 'needleleaf', 'C3', 'C4', 'shrubs', 'lake', 'soil', 'ice', 'canyon', 'roof']
else:
    raise ValueError("tile choice isn't an option")

# for 10 tile
for site in sitechoice:

    site_grids = {}

    for grid in grids:

        if tile_choice == 9:
            landuse = get_landuse_fraction9(site, 'all', grid, file_location)
        elif tile_choice == 10:
            landuse = get_landuse_fraction10(site, 'all', grid, file_location)

        site_grids[grid] = landuse


    csv_name = site + '_' + str(tile_choice) + 'T.csv'
    csv_path = './plots/landuse_csv_files/' + csv_name
    with open(csv_path, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(types)

        for grid in grids:

            new_list = []
            new_list.append(grid)
            for item in site_grids[grid]:
                new_list.append(item)
            filewriter.writerow(new_list)



    land_use_grids(site_grids['A'], site_grids['B'], site_grids['C'], site_grids['D'], site_grids['E'],
                   site_grids['F'],
                   site_grids['G'], site_grids['H'], site_grids['I'], site, tile_choice)

# """

# USE FOR MORPHOLOGY
"""
grids = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

# sitechoice = ['BFCL', 'BCT', 'IML', 'IMU', 'BGH', 'BTT', 'NK', 'RGS', 'KSSW', 'MR', 'SWT']
sitechoice = ['KSSW', 'IMU']
# sitechoice = ['SWINDON']

# 10-tile Maggie old
file_location = '/storage/basic/micromet/Tier_processing/rv006011/landuse/maggie_old/qrparm.urb.morph'
tile_choice = 10

# 10-tile Maggie new
# file_location = '/storage/basic/micromet/Tier_processing/rv006011/landuse/maggie_new/qrparm.urb.morph'
# tile_choice = 10

# WHAT STASH DO YOU WANT
# URBAN BUILDING HEIGHT
# stash = 'm01s00i494'

# URBAN HEIGHT TO WIDTH RATIO
# stash = 'm01s00i495'

# URBAN WIDTH RATIO
stash = 'm01s00i496'

# for 10 tile
for site in sitechoice:

    site_grids = {}

    for grid in grids:
        morph = get_morph_10(site, grid, file_location, stash)
        site_grids[grid] = morph

    csv_name = site + '_' + str(tile_choice) + 'T_morph_' + stash + '_.csv'
    csv_path = '../plots/landuse_csv_files/' + csv_name
    with open(csv_path, 'wb') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['GRID', stash])

        for grid in grids:
            new_list = []
            new_list.append(grid)
            new_list.append(site_grids[grid])
            filewriter.writerow(new_list)
"""




# ORIGINAL CODE SYLVIA SENT TO ME:
# use if wanting to extract an area:
# xu_3 = loc[0]            # lon
# yu_1 = loc[1]            # lat
# xu_4 = loc[0]+0.04       # lon
# yu_2 = loc[1]+0.04       # lat

# rot_pole1 = cube.coord('grid_latitude').coord_system.as_cartopy_crs()
# ll = ccrs.Geodetic()
#
# target_xy1 = rot_pole1.transform_point(xu_3, yu_1, ll) # lower left corner
# x_3 = target_xy1[0] + 360.
# y_1 = target_xy1[1]
# target_xy1 = rot_pole1.transform_point(xu_4, yu_2, ll) # upper right corner
# x_4 = target_xy1[0] + 360.
# y_2 = target_xy1[1]
#
# print x_3
# print y_1
#
# # variables to constraint the loaded variable. Attributes need to be contraint in a different way.
# gcon = iris.Constraint(coord_values={'grid_latitude':lambda cell: y_1 < cell < y_2,
#                                      'grid_longitude':lambda cell: x_3 < cell < x_4})
#
#
# extracted = cube.extract(gcon)
#
# print ' '
# print extracted
# print ' '
#
#
# print extracted.data

# plt.figure(figsize=(10, 20))
# qplt.pcolormesh(extracted[5, 0, 0], vmin=0, vmax=1)
# plt.savefig('ree2.png')

# ----------------------------------------------------------------------------------------------------------------------

# SYLVIA:
# # variables to constraint the loaded variable. Attributes need to be contraint in a different way.
# # See below for stash QH example.
# gcon = iris.Constraint(coord_values={'grid_latitude':lambda cell: y_1 < cell < y_2,
#                                      'grid_longitude':lambda cell: x_3 < cell < x_4})
#
#
#
# if variable == 'QH':
#     hcon = iris.Constraint(coord_values={'grid_latitude':lambda cell: y_1 < cell < y_2,
#                                          'grid_longitude':lambda cell: x_3 < cell < x_4})
# elif variable == 'Tair':
#     hcon = iris.Constraint(coord_values={'grid_latitude':lambda cell: y_1 < cell < y_2,
#                                          'grid_longitude':lambda cell: x_3 < cell < x_4})
#     levcon = iris.Constraint(model_level_number = 1)
