import os
import pandas as pd
import numpy as np
from sklearn.utils import shuffle

DATA_FOLDER = '../data'

def get_data():
    hangover_df = pd.read_csv(os.path.join(DATA_FOLDER, 'hangover/reps.csv'), header=None)
    hangover_df['target'] = 1
    normal_df = pd.read_csv(os.path.join(DATA_FOLDER, 'normal/reps.csv'), header=None)
    normal_df['target'] = 0
    df = pd.concat([hangover_df, normal_df])
    df = shuffle(df)

    msk = np.random.rand(len(df)) <= 0.7
    train_df = df[msk]
    test_df = df[~msk]

    train = {'x': train_df.drop('target', axis=1), 'y': train_df['target']}
    test  = {'x': test_df.drop('target', axis=1), 'y': test_df['target']}
    return train, test

# class Batch:
#     def __init__(self, data):
#         self.data = data
#         self.cur_index = 0
#
#     def next_batch(self, count):
#         res_x = self.data['x'][self.cur_index:self.cur_index+count]
#         res_y = self.data['y'][self.cur_index:self.cur_index+count]
#         self.cur_index = self.cur_index+count
#         return {'x': res_x, 'y': res_y}
#
#     def get_all(self, feature):
#         return self.data[feature]
#
#     def reset(self):
#         self.cur_index = 0
#
#
# hangover = {
#     'train': Batch(train),
#     'test': Batch(test)
# }
