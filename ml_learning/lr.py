"""
This file contains the linear regression implementation
"""

import sys
sys.path.append(".")
from sklearn.model_selection import GridSearchCV
import pandas as pd
import numpy as np
from descriptors import baseline_predictors, random_seed
from sklearn.linear_model import ElasticNet, Ridge, Lasso, HuberRegressor, LinearRegression
from sklearn.svm import LinearSVR
from general import find_optimal_hyperparams, predict

predictors = baseline_predictors


def lr_predict(train_val_csv, train_csv, val_csv, target, linear_model, predictors):
    """
    call on generic hyperparameter search and generic predict to predict any linear model

    input:
        train_val_csv: csv where the training / validation combined dataset is located
        train_csv, val_csv: csv where the training / validation dataset is located
        target: the target variable to predict
        linear_model: a scikitlearn linear model already initialized
        predictors: list of columns to be used for training

    output:
        score: the performance of trained model on validation data based on 'r2' scoring
    """
    # set hyperparameters to search through
    hyper_param_space = {'alpha': 10**np.linspace(1,-3,50)*0.5}
    
    # call on generic hyperparam search
    hyperparams = find_optimal_hyperparams(train_val_csv, target, hyper_param_space, linear_model, predictors)

    # update linear model
    alpha = hyperparams['alpha']
    linear_model.alpha = alpha

    # call on generic predict
    score = predict(train_csv, val_csv, target, linear_model, predictors)
    return score

if __name__ == '__main__':
    # define csvs
    train_val_csv = 'ml_learning/n_train_val.csv'
    train_csv = 'ml_learning/n_train.csv'
    val_csv = 'ml_learning/n_val.csv'

    # define target
    target = 'number_of_rides'

    # declare and run the models
    eln = ElasticNet(random_state = random_seed, max_iter = 10000)
    eln_score = lr_predict(train_val_csv, train_csv, val_csv, target, eln, predictors)

    lss = Lasso(random_state = random_seed, max_iter = 10000)
    lss_score = lr_predict(train_val_csv, train_csv, val_csv, target, lss, predictors)
    
    rdg = Ridge(random_state = random_seed, max_iter = 10000)
    rdg_score = lr_predict(train_val_csv, train_csv, val_csv, target, rdg, predictors)

    hbr = HuberRegressor(max_iter = 10000)
    hbr_score = lr_predict(train_val_csv, train_csv, val_csv, target, hbr, predictors)

    clr = LinearRegression()
    clr_score = predict(train_csv, val_csv, target, clr, predictors)

    svm = LinearSVR(random_state = random_seed, max_iter = 100000)
    svm_score = predict(train_csv, val_csv, target, svm, predictors)

    print(f"'Elastic Net' Score: {eln_score}")
    print(f"'LASSO' Score: {lss_score}")
    print(f"'Ridge' Score: {rdg_score}")
    print(f"'Huber' Score: {hbr_score}")
    print(f"'Classic Linear Regression' Score: {clr_score}")
    print(f"'Support Vector' Score: {svm_score}")