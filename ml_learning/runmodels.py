"""
This file is used to run all models using each type of predictor on validation data to see performance and choose the best model
"""

import sys
sys.path.append(".")
from descriptors import all_predictors, domain_predictors, baseline_predictors, selection_predictors, random_seed
from mlp import find_mlp_optimal_hyperparams, mlp_predict
from sklearn.linear_model import ElasticNet, Ridge, Lasso, HuberRegressor, LinearRegression
from lr import lr_predict
from general import predict
from sklearn.svm import LinearSVR
from sklearn.ensemble import RandomForestRegressor

target = 'number_of_rides'

def test_all_models_on_validation(predictors, predictors_description, train_val_csv, train_csv, val_csv):
    """
    this function is used to run all models with all lists of predictors on validation data using training data
    the best performing model (and only that model) was then tested on test data and reported
    output is saved into a file for easy analysis

    input:
        predictors: list of columns to be used for training
        predictors_description: description in English for each model
        train_val_csv: csv where the training / validation combined dataset is located
        train_csv, val_csv: csv where the training / validation dataset is located
        
    
    output:
        performance saved into a file for analysis
    """
    scores = {}

    # multilayer perceptron
    hyperparams = find_mlp_optimal_hyperparams(train_val_csv, target, predictors)
    mlp_score = mlp_predict(train_csv, val_csv, target, predictors, hyperparams)
    scores[f'{predictors_description} MultiLayer Perceptron'] = mlp_score



    # regression
    eln = ElasticNet(random_state = random_seed, max_iter = 10000)
    eln_score = lr_predict(train_val_csv, train_csv, val_csv, target, eln, predictors)
    scores[f'{predictors_description} Elastic Net Regression'] = eln_score

    lss = Lasso(random_state = random_seed, max_iter = 10000)
    lss_score = lr_predict(train_val_csv, train_csv, val_csv, target, lss, predictors)
    scores[f'{predictors_description} LASSO Regression'] = lss_score
    
    rdg = Ridge(random_state = random_seed, max_iter = 10000)
    rdg_score = lr_predict(train_val_csv, train_csv, val_csv, target, rdg, predictors)
    scores[f'{predictors_description} Ridge Regression'] = rdg_score

    hbr = HuberRegressor(max_iter = 10000)
    hbr_score = lr_predict(train_val_csv, train_csv, val_csv, target, hbr, predictors)
    scores[f'{predictors_description} Huber Regression'] = hbr_score

    clr = LinearRegression()
    clr_score = predict(train_csv, val_csv, target, clr, predictors)
    scores[f'{predictors_description} Classical Linear Regression'] = clr_score

    svm = LinearSVR(random_state = random_seed, max_iter = 100000)
    svm_score = predict(train_csv, val_csv, target, svm, predictors)
    scores[f'{predictors_description} Linear Support Vector'] = svm_score



    # random forest
    rf = RandomForestRegressor(random_state=random_seed)
    rf_score = predict(train_csv, val_csv, target, rf, predictors)
    scores[f'{predictors_description} Random Forest'] = rf_score

    return scores


if __name__ == '__main__':
    all_results = {}

    fs_train_val_csv = 'ml_learning/n_fs_train_val.csv'
    fs_train_csv = 'ml_learning/n_fs_train.csv'
    fs_val_csv = 'ml_learning/n_fs_val.csv'

    train_val_csv = 'ml_learning/n_train_val.csv'
    train_csv = 'ml_learning/n_train.csv'
    val_csv = 'ml_learning/n_val.csv'

    baseline_result = test_all_models_on_validation(baseline_predictors, 'Baseline', train_val_csv, train_csv, val_csv)
    print(baseline_result)
    all_results.update(baseline_result)
    print(all_results)

    selection_result = test_all_models_on_validation(selection_predictors, 'Feature Selection', fs_train_val_csv, fs_train_csv, fs_val_csv)
    print(selection_result)
    all_results.update(selection_result)
    print(all_results)

    all_features_result = test_all_models_on_validation(all_predictors, 'All Features', train_val_csv, train_csv, val_csv)
    print(all_features_result)
    all_results.update(all_features_result)
    print(all_results)

    domain_result = test_all_models_on_validation(domain_predictors, 'Domain Expert', train_val_csv, train_csv, val_csv)
    print(domain_result)
    all_results.update(domain_result)
    print(all_results)

    with open('results.txt', 'w') as file:
        for key, value in all_results.items():
            file.write(f"{key}: {value}\n")

