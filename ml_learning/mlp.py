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

train_val_df = pd.read_csv('ml_learning/n_train_val.csv', dtype={'zip_code': str})

def average_metric(y_true, y_pred):
    mse_y1 = mean_squared_error(y_true[:, 0], y_pred[:, 0])
    mse_y2 = mean_squared_error(y_true[:, 1], y_pred[:, 1])
    average_mse = (mse_y1 + mse_y2) / 2.0
    return -average_mse  # Minimize the negative of the average MSE

def average_r2(y_true, y_pred):
    r2_y1 = r2_score(y_true[:, 0], y_pred[:, 0])
    r2_y2 = r2_score(y_true[:, 1], y_pred[:, 1])
    average_r2 = (r2_y1 + r2_y2) / 2.0
    return -average_r2  # Minimize the negative of the average R-squared


number_of_hidden_layers = [1, 2, 3, 4, 5]
number_of_neurons_per_layer = [20, 50, 100, 200]

# number_of_hidden_layers = [1, 2]
# number_of_neurons_per_layer = [100, 200]

hidden_layer_sizes = []
for layers in number_of_hidden_layers:
    for neurons in number_of_neurons_per_layer:
        layer_size = tuple([neurons] * layers)
        hidden_layer_sizes.append(layer_size)


# Define the scoring function (you can choose either MSE or r2_score)
# Using make_scorer to convert metrics into a scorer object
scoring = {
    'mse_y1': make_scorer(mean_squared_error, greater_is_better=False),
    'mse_y2': make_scorer(mean_squared_error, greater_is_better=False),
    'r2_y1': make_scorer(r2_score),
    'r2_y2': make_scorer(r2_score),
}

mlp = MLPRegressor(random_state=23907251, max_iter=40000, early_stopping = True)

hyper_param_space = {
    'hidden_layer_sizes': hidden_layer_sizes,
    'learning_rate_init':  [0.00001, 0.0001, 0.001, 0.01, 0.1, 0.5]
}

mlp_hyper_search = GridSearchCV(
    estimator = mlp,
    param_grid = hyper_param_space,
    cv = 5,
    n_jobs = -1,
    scoring = 'r2',
    return_train_score = False
) 

mlp_hyper_search.fit(train_val_df[predictors], train_val_df['number_of_rides'])

print(f"Highest scoring hyperparams: {mlp_hyper_search.best_params_} with score: {mlp_hyper_search.best_score_}")