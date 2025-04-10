import os


current_dir = os.getcwd().replace('\\', '/') + '/'


pair_id = 'BCT_IMU'


days_csv_path = current_dir + pair_id + '_days.csv'

assert os.path.isfile(days_csv_path)

print('end')