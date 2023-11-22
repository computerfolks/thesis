import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np
from descriptors import predictors, targets, random_seed
from sklearn.linear_model import ElasticNet, Ridge, Lasso
from general import find_optimal_hyperparams, predict

def find_linear_optimal_hyperparams(train_val_csv, target, linear_model):
    """
    perform gridsearchcv and find optimal hyperparameters for multilayer perceptron
    use 'predictors' from descriptors.py for feature columns

    input:
        train_val_csv: csv where the training / validation combined dataset is located
        target: the target variable to predict

    output:
        mlp_hyper_search.best_params_: optimal hyperparameters found in gridsearchcv
    """
    # set hyperparameters to search through
    hyper_param_space = {'alpha': 10**np.linspace(1,-3,50)*0.5}
    
    # call on generic hyperparam search
    best_params = find_optimal_hyperparams(train_val_csv, target, hyper_param_space, linear_model)
    return best_params


if __name__ == '__main__':
    # define initial model
    eln = ElasticNet(random_state = random_seed, max_iter = 10000)
    train_val_csv = 'ml_learning/n_train_val.csv'
    hyperparams = find_linear_optimal_hyperparams(train_val_csv, 'number_of_rides', eln)
    train_csv = 'ml_learning/n_train.csv'
    val_csv = 'ml_learning/n_val.csv'
    print(hyperparams)
    alpha = hyperparams['alpha']
    eln = ElasticNet(random_state = random_seed, alpha=alpha, max_iter = 10000)
    score = predict(train_csv, val_csv, 'number_of_rides', eln)
    print(score)