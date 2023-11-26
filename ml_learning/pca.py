"""
prelimimary experimentation of PCA - determined to be unhelpful in this instance and scrapped
UNUSED FOR FINAL RESULTS
"""

import sys
sys.path.append(".")
from sklearn.linear_model import ElasticNet
from sklearn.decomposition import PCA
import pandas as pd
from descriptors import predictors, random_seed

train_val_csv = 'ml_learning/n_train_val.csv'
train_csv = 'ml_learning/n_train.csv'
val_csv = 'ml_learning/n_val.csv'

train_df = pd.read_csv(train_csv, dtype={'zip_code': str})
val_df = pd.read_csv(val_csv, dtype={'zip_code': str})
train_val_df = pd.read_csv(train_val_csv, dtype={'zip_code': str})

pca = PCA(svd_solver='full')
pca.fit(train_df[predictors])

eln = ElasticNet(random_state = random_seed, max_iter = 10000)
target = 'number_of_rides'

x_train = pca.transform(train_df[predictors])
y_train = train_df[target]
eln.fit(x_train, y_train)

x_val = pca.transform(val_df[predictors])
y_val = val_df[target]

score = eln.score(x_val, y_val)
print(score)