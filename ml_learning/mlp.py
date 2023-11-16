import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer, mean_squared_error, r2_score
import pandas as pd
from descriptors import predictors, targets


def find_optimal_hyperparams(train_val_csv, target):
    """
    perform gridsearchcv and find optimal hyperparameters for multilayer perceptron
    use 'predictors' from descriptors.py for feature columns

    input:
        train_val_csv: csv where the training / validation combined dataset is located
        target: the target variable to predict

    output:
        mlp_hyper_search.best_params_: optimal hyperparameters found in gridsearchcv
    """
    # read csv
    train_val_df = pd.read_csv(train_val_csv, dtype={'zip_code': str})

    # set scoring, 'r2' and 'neg_mean_squared_error' both available
    scoring = 'r2'

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

    mlp = MLPRegressor(random_state=23907251, max_iter=40000, early_stopping = True)
    mlp_hyper_search = GridSearchCV(
        estimator = mlp,
        param_grid = hyper_param_space,
        cv = 5,
        n_jobs = -1,
        scoring = scoring,
        return_train_score = False
    ) 
    mlp_hyper_search.fit(train_val_df[predictors], train_val_df[target])
    print(f"Highest scoring hyperparams: {mlp_hyper_search.best_params_} with score: {mlp_hyper_search.best_score_}")

    return mlp_hyper_search.best_params_

def mlp_predict(train_csv, val_csv, target, hyperparams=None):
    """
    build and predict using mlp. use predetermined hyperparameters

    input:
        train_csv: file that has the training data
        val_csv: file that has the validation data
        target: variable to predict
    
    output:
        r2 score between predictions and actual values for validation dataset
    """
    train_df = pd.read_csv(train_csv, dtype={'zip_code': str})
    val_df = pd.read_csv(val_csv, dtype={'zip_code': str})

    # either use hyperparams search, or if it was already performed, use values found from previous search that were manually written in
    if hyperparams is not None:
        hidden_layer_sizes = hyperparams['hidden_layer_sizes']
        learning_rate_init = hyperparams['learning_rate_init']
    else:
        hidden_layer_sizes = (200, 200, 200, 200, 200)
        learning_rate_init = 0.001
    
    
    regr = MLPRegressor(random_state=23907251, max_iter=40000, hidden_layer_sizes=hidden_layer_sizes, learning_rate_init=learning_rate_init)
    regr.fit(train_df[predictors], train_df[target])
    val_df_target_actual = val_df[target]
    print(regr.score(val_df[predictors], val_df_target_actual))

if __name__ == '__main__':
    train_val_csv = 'ml_learning/n_train_val.csv'
    hyperparams = find_optimal_hyperparams(train_val_csv, 'number_of_rides')
    train_csv = 'ml_learning/n_train.csv'
    val_csv = 'ml_learning/n_val.csv'
    mlp_predict(train_csv, val_csv, 'number_of_rides', hyperparams)