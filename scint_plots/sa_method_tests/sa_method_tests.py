import os
import scintools as sct
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib as mpl

mpl.rcParams.update({'font.size': 15})


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

    # plotting
    fig = plt.figure(figsize=(15, 12))
    spec = gridspec.GridSpec(ncols=2, nrows=2)

    ax1 = plt.subplot(spec[0])
    ax2 = plt.subplot(spec[1])
    ax3 = plt.subplot(spec[2])
    ax4 = plt.subplot(spec[3])

    linestyles = {'constant': '--', 'varying': '-'}
    markers = {'constant': 'o', 'varying': 'x'}
    colours = {'IOP1': 'red', 'IOP2': 'blue'}

    # zd
    # IOP1
    ax1.plot(df.index.values, df.z_d_123_constant.values, marker=markers['constant'], linestyle=linestyles['constant'],
             color=colours['IOP1'])
    ax1.plot(df.index.values, df.z_d_123_varying.values, marker=markers['varying'], color=colours['IOP1'],
             linestyle=linestyles['varying'])
    # IOP2
    ax1.plot(df.index.values, df.z_d_126_constant.values, marker=markers['constant'], linestyle=linestyles['constant'],
             color=colours['IOP2'])
    ax1.plot(df.index.values, df.z_d_126_varying.values, marker=markers['varying'], color=colours['IOP2'],
             linestyle=linestyles['varying'])

    ax1.plot([], [], color=colours['IOP1'], label='IOP-1')
    ax1.plot([], [], color=colours['IOP2'], label='IOP-1')
    ax1.legend()

    ax1.set_ylabel('z$_{d}$ (m)')

    # z0
    # IOP1
    ax2.plot(df.index.values, df.z_0_123_constant.values, marker=markers['constant'], linestyle=linestyles['constant'],
             color=colours['IOP1'])
    ax2.plot(df.index.values, df.z_0_123_varying.values, marker=markers['varying'], color=colours['IOP1'],
             linestyle=linestyles['varying'])
    # IOP2
    ax2.plot(df.index.values, df.z_0_126_constant.values, marker=markers['constant'], linestyle=linestyles['constant'],
             color=colours['IOP2'])
    ax2.plot(df.index.values, df.z_0_126_varying.values, marker=markers['varying'], color=colours['IOP2'],
             linestyle=linestyles['varying'])

    ax2.plot([], [], color='black', marker=markers['constant'], linestyle=linestyles['constant'],
             label='EC fp constant')
    ax2.plot([], [], color='black', marker=markers['varying'], linestyle=linestyles['varying'], label='EC fp varying')
    ax2.legend()

    ax2.set_ylabel('z$_{0}$ (m)')

    # percentage difference

    df['per_diff_zd_123'] = percentage_change(df['z_d_123_varying'], df['z_d_123_constant'])
    df['per_diff_zd_126'] = percentage_change(df['z_d_126_varying'], df['z_d_126_constant'])

    df['per_diff_z0_123'] = percentage_change(df['z_0_123_varying'], df['z_0_123_constant'])
    df['per_diff_z0_126'] = percentage_change(df['z_0_126_varying'], df['z_0_126_constant'])

    # plot

    # zd
    # I0P1
    ax3.plot(df.index.values, df.per_diff_zd_123.values, marker='D', color=colours['IOP1'])

    # IOP2
    ax3.plot(df.index.values, df.per_diff_zd_126.values, marker='D', color=colours['IOP2'])

    ax3.set_ylabel('% difference in z$_{d}$ (%)')

    # z0
    # I0P1
    ax4.plot(df.index.values, df.per_diff_z0_123.values, marker='D', color=colours['IOP1'])
    # IOP2
    ax4.plot(df.index.values, df.per_diff_z0_126.values, marker='D', color=colours['IOP2'])

    ax4.set_ylabel('% difference in z$_{0}$ (%)')

    ax3.set_xlabel('Time (h, UTC)')
    ax4.set_xlabel('Time (h, UTC)')

    fig.subplots_adjust(wspace=0.28, hspace=0)

    plt.savefig('./sa_method_tests.png', bbox_inches='tight', dpi=300)

    print('end')


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
