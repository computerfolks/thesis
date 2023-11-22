import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from sklearn.ensemble import RandomForestRegressor
from descriptors import random_seed
from general import predict

if __name__ == '__main__':
    train_csv = 'ml_learning/n_train.csv'
    val_csv = 'ml_learning/n_val.csv'
    rf = RandomForestRegressor(random_state=random_seed)
    print(predict(train_csv, val_csv, 'number_of_rides', rf))
    
