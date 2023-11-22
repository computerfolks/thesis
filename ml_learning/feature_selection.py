import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectPercentile, mutual_info_classif
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
from descriptors import all_predictors

target = 'number_of_rides'

fs_tune_csv = 'ml_learning/n_fs_tune.csv'
fs_tune_df = pd.read_csv(fs_tune_csv, dtype={'zip_code': str})

x_tune = fs_tune_df[all_predictors]
y_tune = fs_tune_df[target]

predictors_plus_target = all_predictors.copy()
predictors_plus_target.append(target)

correlation_matrix = fs_tune_df[predictors_plus_target].corr()
print(correlation_matrix['number_of_rides'])