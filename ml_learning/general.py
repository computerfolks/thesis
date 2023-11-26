import sys
sys.path.append(".")
import pandas as pd
from sklearn.model_selection import GridSearchCV
import pickle

def find_optimal_hyperparams(train_val_csv, target, hyper_param_space, initialized_model, predictors):
    """
    generic function to perform gridsearchcv and find optimal hyperparameters for initialized_model

    input:
        train_val_csv: csv where the training / validation combined dataset is located
        target: the target variable to predict
        hyper_param_space: the hyperparameter space to search through
        initialized_model: an ML model already initialized and ready to be fit / trained
        predictors: list of columns to be used for training

    output:
        mlp_hyper_search.best_params_: optimal hyperparameters found in gridsearchcv
    """
    # read csv
    train_val_df = pd.read_csv(train_val_csv, dtype={'zip_code': str})

    # define scoring, can be 'r2' or many other options, to view options enter invalid string and scikitlearn will print all options
    scoring = 'r2'

    hyper_search = GridSearchCV(
        estimator = initialized_model,
        param_grid = hyper_param_space,
        cv = 5,
        n_jobs = -1,
        scoring = scoring,
        return_train_score = False
    ) 

    hyper_search.fit(train_val_df[predictors], train_val_df[target])
    print(f"Highest scoring hyperparams: {hyper_search.best_params_} with score: {hyper_search.best_score_}")

    return hyper_search.best_params_


def predict(train_csv, val_csv, target, initialized_model, predictors):
    """
    generic function to train and predict a target variable given an initialized model (with hyperparams already specified) ready to be trained / fit

    input:
        train_csv, val_csv: csv where the training / validation dataset is located
        target: the target variable to predict
        initialized_model: an ML model already initialized and ready to be fit / trained
        predictors: list of columns to be used for training

    output:
        score: the performance of trained model on validation data based on 'r2'
    """
    train_df = pd.read_csv(train_csv, dtype={'zip_code': str})
    val_df = pd.read_csv(val_csv, dtype={'zip_code': str})

    x_train = train_df[predictors]
    y_train = train_df[target]
    initialized_model.fit(x_train, y_train)

    # use this when saving the results of the model for testing real life cases
    # with open('ml_learning/model.pkl', 'wb') as file:
    #     pickle.dump(initialized_model, file)

    x_val = val_df[predictors]
    y_val = val_df[target]

    score = initialized_model.score(x_val, y_val)
    return score