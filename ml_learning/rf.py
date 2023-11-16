import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from descriptors import predictors, targets

def rf_predict(target):
    rf = RandomForestRegressor(random_state=23907251)
    train_df = pd.read_csv('ml_learning/n_train.csv', dtype={'zip_code': str})
    val_df = pd.read_csv('ml_learning/n_val.csv', dtype={'zip_code': str})

    x_train = train_df[predictors]
    y_train = train_df[target]
    rf.fit(x_train, y_train)

    x_val = val_df[predictors]
    y_val = val_df[target]
    # y_pred = rf.predict(x_val)

    print(rf.score(x_val, y_val))

if __name__ == '__main__':
    rf_predict('total_length')
    
