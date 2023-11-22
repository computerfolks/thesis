import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer, mean_squared_error, r2_score
import pandas as pd
from descriptors import predictors, targets, random_seed
from general import find_optimal_hyperparams, predict


def find_mlp_optimal_hyperparams(train_val_csv, target):
    """
    specify conditions for multilayer perceptron gridsearchcv
    utilize generic 'find_optimal_hyperparams' for search

    input:
        train_val_csv: csv where the training / validation combined dataset is located
        target: the target variable to predict

    output:
        best_params: the optimal hyperparameters found by find_optimal_hyperparams
    """
    # set hyperparameters to search through
    number_of_hidden_layers = [1, 2, 3, 4, 5]
    number_of_neurons_per_layer = [2, 5, 10, 20, 50, 100, 200, 400]

    # formulate hidden layer sizes in proper format
    hidden_layer_sizes = []
    for layers in number_of_hidden_layers:
        for neurons in number_of_neurons_per_layer:
            layer_size = tuple([neurons] * layers)
            hidden_layer_sizes.append(layer_size)

    # define hyper param space
    hyper_param_space = {
        'hidden_layer_sizes': hidden_layer_sizes,
        'learning_rate_init':  [0.00001, 0.0001, 0.001, 0.01, 0.1, 0.5]
    }

    # define initial model
    mlp = MLPRegressor(random_state=random_seed, max_iter=40000, early_stopping = True)

    # call on generic hyperparam search
    best_params = find_optimal_hyperparams(train_val_csv, target, hyper_param_space, mlp)
    return best_params

def mlp_predict(train_csv, val_csv, target, hyperparams=None):
    """
    specify conditions for multilayer perceptron prediction
    utilize generic 'predict' for prediction

    input:
        train_csv: file that has the training data
        val_csv: file that has the validation data
        target: variable to predict
    
    output:
        score: the performance of trained model on validation data
    """
    # either use hyperparams search, or if it was already performed, use values found from previous search that were manually written in
    if hyperparams is not None:
        hidden_layer_sizes = hyperparams['hidden_layer_sizes']
        learning_rate_init = hyperparams['learning_rate_init']
    else:
        # hidden_layer_sizes = (200, 200, 200, 200, 200)
        # learning_rate_init = 0.001  
        hidden_layer_sizes = (10, 10, 10, 10)
        learning_rate_init = 0.01 

    # define initial model
    regr = MLPRegressor(random_state=random_seed, max_iter=40000, hidden_layer_sizes=hidden_layer_sizes, learning_rate_init=learning_rate_init)
    
    score = predict(train_csv, val_csv, target, regr)
    return score

if __name__ == '__main__':
    train_val_csv = 'ml_learning/n_fs_train_val.csv'
    hyperparams = find_mlp_optimal_hyperparams(train_val_csv, 'number_of_rides')
    train_csv = 'ml_learning/n_fs_train.csv'
    val_csv = 'ml_learning/n_fs_val.csv'
    score = mlp_predict(train_csv, val_csv, 'number_of_rides', hyperparams)
    print(score)