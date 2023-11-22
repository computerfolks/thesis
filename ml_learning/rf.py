import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from sklearn.ensemble import RandomForestRegressor
from descriptors import random_seed, baseline_predictors, selection_predictors, domain_predictors
from general import predict
import pickle
import pandas as pd

predictors = selection_predictors

if __name__ == '__main__':
    train_csv = 'ml_learning/n_train_val.csv'
    test_csv = 'ml_learning/n_test.csv'
    rf = RandomForestRegressor(random_state=random_seed)
    print(predict(train_csv, test_csv, 'number_of_rides', rf, predictors))

    with open('ml_learning/model.pkl', 'rb') as file:
        model = pickle.load(file)
        test_df = pd.read_csv(test_csv, dtype={'zip_code': str})
        x_val = test_df[predictors]
        y_val = test_df['number_of_rides']

        score = model.score(x_val, y_val)
        print(score)


    
