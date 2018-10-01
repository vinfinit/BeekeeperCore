import os
import pandas as pd
import numpy as np

from sklearn import linear_model
from sklearn import svm
from sklearn import ensemble
from sklearn.utils import shuffle
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib

from core import preprocessing

MODEL_FOLDER = '../models'
train, test = preprocessing.get_data()

model = ensemble.RandomForestRegressor(n_estimators=50, max_depth=3)
model.fit(train['x'], train['y'])

train['pred'] = model.predict(train['x'])
test['pred'] = model.predict(test['x'])

print('Train error', mean_squared_error(train['y'], train['pred']))
print('Test error', mean_squared_error(test['y'], test['pred']))

joblib.dump(model, os.path.join(MODEL_FOLDER, 'random_forest.pkl'), protocol=2)
