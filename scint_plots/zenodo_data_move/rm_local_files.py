# script to remove London model files from zenodo location
# DANGEROUS FILE DONT EXECUTE UNLESS YOU KNOW WHAT YOU'RE DOING
# 09-04-2025


import os

root_filepath = 'D:/zenodo/P2 CASES/UKV/2018/'

DOY_filepaths = [f.path + '/' for f in os.scandir(root_filepath) if f.is_dir()]

for DOY_filepath in DOY_filepaths:

    print(DOY_filepath)

    # check file path exists
    assert os.path.isdir(DOY_filepath)

    all_files = [f for f in os.listdir(DOY_filepath) if os.path.isfile(os.path.join(DOY_filepath, f))]

    LON_files = []

    for file in all_files:

        if file[:5] == 'MOLON':
            LON_files.append(DOY_filepath + file)

    for LON_file in LON_files:
        os.remove(LON_file)

print('end')
