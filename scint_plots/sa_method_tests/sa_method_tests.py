import os
import scintools as sct
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib as mpl
import numpy as np
from scint_flux import run_function

mpl.rcParams.update({'font.size': 15})


def retrieve_z_fb(path='BCT_IMU'):
    """

    :return:
    """

    bdsm_path = 'D:/Documents/scintools/example_inputs/rasters/height_surface_4m.tif'
    cdsm_path = 'D:/Documents/scintools/example_inputs/rasters/height_veg_4m.tif'
    dem_path = 'D:/Documents/scintools/example_inputs/rasters/height_terrain_4m.tif'

    scint_path_dict = run_function.construct_path(path, bdsm_path, cdsm_path, dem_path)

    z_fb = scint_path_dict['z_fb']

    return z_fb


def percentage_change(col1, col2):
    """

    :param col1:
    :param col2:
    :return:
    """
    return ((col2 - col1) / col1) * 100


def find_sas(sa_test_dir, DOY):
    """

    :return:
    """

    file_list = []
    for file in os.listdir(sa_test_dir):
        if file.endswith(".tif"):
            if str(DOY) in file:
                file_list.append(file[:-4])

    return file_list


def read_roughness(sa_test_dir, file_list, DOY, test):
    """

    :return:
    """

    hours = []
    z_0_list = []
    z_d_list = []

    for file in file_list:
        file_path = sa_test_dir + file

        # assert file exists
        assert os.path.isfile(file_path + '.tif')

        # read footprint
        reference_footprint_read = sct.read_footprint(file_path)

        z_0 = reference_footprint_read.roughness_outputs.z_0
        z_d = reference_footprint_read.roughness_outputs.z_d

        hours.append(file.split('_')[-2])
        z_0_list.append(z_0)
        z_d_list.append(z_d)

    if test:
        test_str = 'constant'
    else:
        test_str = 'varying'

    # create df
    df_dict = {'hour': hours, 'z_0_' + str(DOY) + '_' + test_str: z_0_list,
               'z_d_' + str(DOY) + '_' + test_str: z_d_list}
    df = pd.DataFrame.from_dict(df_dict)

    df.index = df.hour.astype('int')
    df = df.drop(columns=['hour'])

    return df


def plot_method_tests(df):
    """

    :return:
    """

    # percentage difference

    df['per_diff_zd_123'] = percentage_change(df['z_d_123_varying'], df['z_d_123_constant'])
    df['per_diff_zd_126'] = percentage_change(df['z_d_126_varying'], df['z_d_126_constant'])

    df['per_diff_z0_123'] = percentage_change(df['z_0_123_varying'], df['z_0_123_constant'])
    df['per_diff_z0_126'] = percentage_change(df['z_0_126_varying'], df['z_0_126_constant'])

    print('zd range: ', min([np.abs(df['per_diff_zd_126']).min(), np.abs(df['per_diff_zd_123']).min()]), ' to ',
          max([np.abs(df['per_diff_zd_126']).max(), np.abs(df['per_diff_zd_123']).max()]))
    print('z0 range: ', min([np.abs(df['per_diff_z0_126']).min(), np.abs(df['per_diff_z0_123']).min()]), ' to ',
          max([np.abs(df['per_diff_z0_126']).max(), np.abs(df['per_diff_z0_123']).max()]))

    stats_zd = pd.concat([df['per_diff_zd_126'], df['per_diff_zd_123']]).dropna()
    over_10_zd = len(np.where(np.abs(stats_zd) > 10)[0])
    print('zd ', over_10_zd, ' out of ', len(stats_zd))

    stats_z0 = pd.concat([df['per_diff_z0_126'], df['per_diff_z0_123']]).dropna()
    over_10_z0 = len(np.where(np.abs(stats_z0) > 10)[0])
    print('z0 ', over_10_z0, ' out of ', len(stats_z0))

    # get effective beam height
    z_fb = retrieve_z_fb()

    # adding these to the sa method test df
    df['z_f_123_constant'] = z_fb - df.z_d_123_constant
    df['z_f_126_constant'] = z_fb - df.z_d_126_constant

    df['z_f_123_varying'] = z_fb - df.z_d_123_varying
    df['z_f_126_varying'] = z_fb - df.z_d_126_varying

    df['per_diff_zf_123'] = percentage_change(df['z_f_123_varying'], df['z_f_123_constant'])
    df['per_diff_zf_126'] = percentage_change(df['z_f_126_varying'], df['z_f_126_constant'])

    stats_zf = pd.concat([df['per_diff_zf_126'], df['per_diff_zf_123']]).dropna()

    print('zf range: ', min(np.abs(stats_zf)), ' to ', max(np.abs(stats_zf)))

    # plotting
    fig = plt.figure(figsize=(15, 12))
    spec = gridspec.GridSpec(ncols=2, nrows=3)

    ax1 = plt.subplot(spec[0])
    ax2 = plt.subplot(spec[1])
    ax3 = plt.subplot(spec[2])
    ax4 = plt.subplot(spec[3])
    ax5 = plt.subplot(spec[4])
    ax6 = plt.subplot(spec[5])

    linestyles = {'constant': ':', 'varying': '-'}
    markers = {'constant': 'o', 'varying': 'o'}
    colours = {'IOP1': 'red', 'IOP2': 'blue'}

    # z0
    # IOP1
    ax1.plot(df.index.values, df.z_0_123_constant.values, marker=markers['constant'], linestyle=linestyles['constant'],
             color=colours['IOP1'], markerfacecolor='white')
    ax1.plot(df.index.values, df.z_0_123_varying.values, marker=markers['varying'], color=colours['IOP1'],
             linestyle=linestyles['varying'])
    # IOP2
    ax1.plot(df.index.values, df.z_0_126_constant.values, marker=markers['constant'], linestyle=linestyles['constant'],
             color=colours['IOP2'],  markerfacecolor='white')
    ax1.plot(df.index.values, df.z_0_126_varying.values, marker=markers['varying'], color=colours['IOP2'],
             linestyle=linestyles['varying'])

    ax1.plot([], [], color='black', marker=markers['constant'], linestyle=linestyles['constant'],  markerfacecolor='white',
             label='$SA_{LAS}^{old}$')
    ax1.plot([], [], color='black', marker=markers['varying'], linestyle=linestyles['varying'],
             label='$SA_{LAS}$')
    ax1.legend()

    ax1.set_ylabel('z$_{0}$ (m)')

    # z0 % diff
    # I0P1
    ax2.plot(df.index.values, df.per_diff_z0_123.values, marker='D', color=colours['IOP1'])
    # IOP2
    ax2.plot(df.index.values, df.per_diff_z0_126.values, marker='D', color=colours['IOP2'])

    ax2.set_ylabel('Difference in z$_{0}$ (%)')

    ax2.plot([], [], color=colours['IOP1'], label='IOP-1')
    ax2.plot([], [], color=colours['IOP2'], label='IOP-2')
    ax2.legend()

    # zd
    # IOP1
    ax3.plot(df.index.values, df.z_d_123_constant.values, marker=markers['constant'], linestyle=linestyles['constant'],
             color=colours['IOP1'], markerfacecolor='white')
    ax3.plot(df.index.values, df.z_d_123_varying.values, marker=markers['varying'], color=colours['IOP1'],
             linestyle=linestyles['varying'])
    # IOP2
    ax3.plot(df.index.values, df.z_d_126_constant.values, marker=markers['constant'], linestyle=linestyles['constant'],
             color=colours['IOP2'],  markerfacecolor='white')
    ax3.plot(df.index.values, df.z_d_126_varying.values, marker=markers['varying'], color=colours['IOP2'],
             linestyle=linestyles['varying'])

    ax3.set_ylabel('z$_{d}$ (m)')

    # zd % diff
    # I0P1
    ax4.plot(df.index.values, df.per_diff_zd_123.values, marker='D', color=colours['IOP1'])

    # IOP2
    ax4.plot(df.index.values, df.per_diff_zd_126.values, marker='D', color=colours['IOP2'])

    ax4.set_ylabel('Difference in z$_{d}$ (%)')

    # zf
    # IOP1
    ax5.plot(df.index.values, df.z_f_123_constant.values, marker=markers['constant'], linestyle=linestyles['constant'],
             color=colours['IOP1'],  markerfacecolor='white')
    ax5.plot(df.index.values, df.z_f_123_varying.values, marker=markers['varying'], color=colours['IOP1'],
             linestyle=linestyles['varying'])
    # IOP2
    ax5.plot(df.index.values, df.z_f_126_constant.values, marker=markers['constant'], linestyle=linestyles['constant'],
             color=colours['IOP2'],  markerfacecolor='white')
    ax5.plot(df.index.values, df.z_f_126_varying.values, marker=markers['varying'], color=colours['IOP2'],
             linestyle=linestyles['varying'])

    ax5.set_ylabel('z$_{f}$ (m)')

    # zf % diff
    # I0P1
    ax6.plot(df.index.values, df.per_diff_zf_123.values, marker='D', color=colours['IOP1'])

    # IOP2
    ax6.plot(df.index.values, df.per_diff_zf_126.values, marker='D', color=colours['IOP2'])

    ax6.set_ylabel('Difference in z$_{f}$ (%)')

    ax5.set_xlabel('Time (h, UTC)')
    ax6.set_xlabel('Time (h, UTC)')

    fig.subplots_adjust(wspace=0.28, hspace=0)

    plt.savefig('./sa_method_tests.png', bbox_inches='tight', dpi=300)

    print('end')


if __name__ == '__main__':
    current_dir = os.getcwd().replace('\\', '/') + '/'
    sa_test_dir = current_dir + 'SA_constant/'

    file_list_test_123 = find_sas(sa_test_dir, 123)
    df_test_123 = read_roughness(sa_test_dir, file_list_test_123, 123, test=True)

    file_list_test_126 = find_sas(sa_test_dir, 126)
    df_test_126 = read_roughness(sa_test_dir, file_list_test_126, 126, test=True)

    sa_used_dir_123 = 'C:/Users/beths/OneDrive - University of Reading/local_runs_data/fp_output/hourly/2016' + '123' + '/'
    sa_used_dir_126 = 'C:/Users/beths/OneDrive - University of Reading/local_runs_data/fp_output/hourly/2016' + '126' + '/'

    file_list_real_123 = find_sas(sa_used_dir_123, 123)
    file_list_real_126 = find_sas(sa_used_dir_126, 126)

    df_real_123 = read_roughness(sa_used_dir_123, file_list_real_123, 123, test=False)
    df_real_126 = read_roughness(sa_used_dir_126, file_list_real_126, 126, test=False)

    df = pd.concat([df_test_123, df_test_126, df_real_123, df_real_126], axis=1)

    plot_method_tests(df)

    print('end')
