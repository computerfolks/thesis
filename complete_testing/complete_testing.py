"""
this file contains all necessary functionality to test the package
when able, other functions are imported
when necessary, new functions were written to make start-to-finish testing functional
"""


import sys
sys.path.append(".")
from plotting.plot_one_metric import plot_metric_by_multiple_intervals, plot_metric_by_single_interval, get_formatted_date_without_year
from plotting.test_dictionary_pre_dataframe import test_dictionary_seven
from user.user_input import get_date_range_keys_zip_codes_values_dictionary
from query import get_query_results_for_date_range_zip_codes_dict
from convert_to_dataframe import clean_convert_dictionary_to_dataframe
from descriptors import start_stations_to_zips, graphable_columns, selection_predictors
import pandas as pd
from ml_normalize.split import fit_and_trans
import pickle
from scipy.stats import norm

target = 'number_of_rides'

def extract_zips(user_dict):
    """
    function to extract the zip codes from a user_dict
    """
    unique_zip_codes = set()
    
    # lists of zip codes are found in the values() of the user_dict dictionary
    for zip_codes_list in user_dict.values():
        # go through the list
        for zip_code in zip_codes_list:
            unique_zip_codes.add(zip_code)
    return unique_zip_codes

def has_one_interval(user_dict):
    """
    function which determines if the user_dict has more than one MM-DD to MM-DD interval
    used to determine whether plot_one_interval or plot_multiple_intervals should be used
    """
    unique_intervals = set()

    for start_date, end_date in user_dict.keys():
        start_date_without_year = get_formatted_date_without_year(start_date)
        end_date_without_year = get_formatted_date_without_year(end_date)

        start_end_without_year = (start_date_without_year, end_date_without_year)
        
        unique_intervals.add(start_end_without_year)

    # if length of set is 1, there is only one unique interval
    return len(unique_intervals) == 1


def bike_rides_available(zips):
    """
    function to check if bike rides will be usable
    bike rides are only allowed if the stations were used in training
    all zip codes must be able to show bike data for the function to return true
    """
    bike = True
    for zip_code in zips:
        if zip_code not in start_stations_to_zips.values():
            bike = False
    return bike


def metric_to_plot(bike_rides_available):
    """
    collect a metric that will be plotted
    ensure the metric is valid
    add bikerides if bike_rides_available is true
    """
    columns_to_choose = graphable_columns.copy()
    if bike_rides_available:
        columns_to_choose.append('bikerides')

    valid_column = False
    while valid_column is False:
        print("Enter the metric you would like to plot. You must choose from the following list: ")
        print(columns_to_choose)
        column = input()
        if column in columns_to_choose:
            return column
        else:
            print(f"{column} not found in list. Please try again.")

def ask_user_if_more_metrics():
    """
    ask user if more metrics should be graphed, or if user wants program to exit, output T/F
    """
    answer = input("To graph more metrics, type 'y' and press enter. Otherwise, type any other key and press enter: ")
    if answer.lower() == 'y':
        return True
    else:
        return False
    

def get_stats_from_training(train_val_csv, current_zip_code):
    """
    collect basic statistics for a zip code from training data
    """
    train_val_df = pd.read_csv(train_val_csv, dtype={'zip_code': str})
    filtered_df = train_val_df[train_val_df['zip_code'] == current_zip_code]
    median_value = filtered_df[target].median()
    average_value = filtered_df[target].mean()
    std_deviation_value = filtered_df[target].std()
    return median_value, average_value, std_deviation_value

    
def predict_real_example(df):
    """
    use saved model to predict values for each row
    """
    with open('ml_learning/model.pkl', 'rb') as file:
        # load model that was created and saved
        model = pickle.load(file)

        # predictors
        x_val = df[selection_predictors]

        y_pred = model.predict(x_val)
        return y_pred
    

def normalize_weather_dataframe_always_true(df):
    """
    a slice of normalize_weather_dataframe from ml_preprocessing/weather
    only use the slice that is always true without any scaling
    """
    # define normalization instructions
    columns_to_divide_by_100 = ['humidity', 'precipcover', 'cloudcover']
    columns_to_divide_by_10 = ['uvindex']

    # normalize
    df[columns_to_divide_by_100] /= 100
    df[columns_to_divide_by_10] /= 10

    return df


def add_bike_rides(dataframe, n_train_val_csv, unnormalized_train_val_csv, zip_codes_list):
    """
    function to add bike ride predictions to the dataframe
    NOTE: missing weather data due to collection errors will lead to exceptions and exiting

    input:
        dataframe: the current weather dataframe
        n_train_val_csv: the normalized csv that comes out of split.py which stores the training data
        unnormalized_train_val_csv: the raw csv that comes out of dataframe.py before scaling
        zip_codes_list: list of all zip codes in the dataframe
    """
    # define empty columns
    dataframe['median'] = None
    dataframe['average'] = None
    dataframe['std'] = None

    # use normalized to get the statistics, since normalized dataframe is used when z-score and percentile are calculated
    for current_zip_code in zip_codes_list:
        # for each zip code, collect median, standard dev, and average and add to the dataframe
        median, average, std = get_stats_from_training(n_train_val_csv, current_zip_code)

        dataframe.loc[dataframe['zip_code'] == current_zip_code, 'median'] = median
        dataframe.loc[dataframe['zip_code'] == current_zip_code, 'average'] = average
        dataframe.loc[dataframe['zip_code'] == current_zip_code, 'std'] = std

    # use unnormalized to report stats to user
    for current_zip_code in zip_codes_list:
        median, average, std = get_stats_from_training(unnormalized_train_val_csv, current_zip_code)
        print(f"Zip Code {current_zip_code} Median: {median}")
        print(f"Zip Code {current_zip_code} Average: {average}")
        print(f"Zip Code {current_zip_code} Standard Deviation: {std}")

    # save dataframe to temp csv to fit function format
    path = 'complete_testing/temp.csv'
    normalized_always_true_dataframe = normalize_weather_dataframe_always_true(dataframe.copy(deep = True))
    dataframe.to_csv(path, index=False)

    # transform dataframe by fitting on training
    trans_dataframe = fit_and_trans(unnormalized_train_val_csv, path, None, 'complete_testing/trans.csv', real_example=True)

    # predict the 'number_of_rides'
    predictions = predict_real_example(trans_dataframe)
    trans_dataframe[target] = predictions

    # calculate the z-score for each value in the target column
    trans_dataframe['zscore'] = (trans_dataframe[target] - trans_dataframe['average']) / trans_dataframe['std']

    # calculate the z-score percentile using the cdf
    trans_dataframe['zscore_percentile'] = norm.cdf(trans_dataframe['zscore']) * 100

    # use the saved scalers that were stored when running split.py
    for current_zip_code in zip_codes_list:
        with open(f'complete_testing/robust_scaler_{current_zip_code}.pkl', 'rb') as file:
            loaded_scaler = pickle.load(file)
            # inverse_transform the target for the current zip code, numpy and reshape as needed
            trans_dataframe.loc[trans_dataframe['zip_code'] == current_zip_code, target] = loaded_scaler.inverse_transform(trans_dataframe.loc[trans_dataframe['zip_code'] == current_zip_code, target].to_numpy().reshape(-1, 1))

    # add the values found to the current dataframe that are relevant
    # the dataframe returned needs to have raw, untransformed weather data
    # so one cannot simply return the trans_dataframe
    dataframe['number_of_rides'] = trans_dataframe['number_of_rides']
    dataframe['zscore_percentile'] = trans_dataframe['zscore_percentile']

    return dataframe


if __name__ == '__main__':
    # collect user_dict of zip codes and intervals
    user_dict = get_date_range_keys_zip_codes_values_dictionary()

    # determine if there is one interval of MM-DD or not
    one_interval = has_one_interval(user_dict)

    # collect unique zip codes
    zips = extract_zips(user_dict)

    # determine if bike_ride data is available (only true if all zips have been trained on)
    bike_ride = bike_rides_available(zips)

    # query for weather data
    new_user_query_results = get_query_results_for_date_range_zip_codes_dict(user_dict)

    # convert to dataframe
    new_user_dataframe = clean_convert_dictionary_to_dataframe(new_user_query_results)

    # ensure bike rides are only added once
    bike_rides_already_added = False
    # plot as long as user wants more metrics plotted
    keep_plotting = True
    
    while(keep_plotting):
        metric = metric_to_plot(bike_ride)
        if metric == 'bikerides' and bike_rides_already_added is False:
            # use non-normalized to get proper metrics to report to user
            new_user_dataframe = add_bike_rides(new_user_dataframe, 'ml_learning/n_fs_train_val.csv', 'ml_normalize/fs_train_val.csv', zips)
            bike_rides_already_added = True
        if one_interval:
            if metric == 'bikerides':
                plot_metric_by_single_interval(new_user_dataframe, 'number_of_rides')
                plot_metric_by_single_interval(new_user_dataframe, 'zscore_percentile')
            else:
                plot_metric_by_single_interval(new_user_dataframe, metric)
        else:
            if metric == 'bikerides':
                plot_metric_by_multiple_intervals(new_user_dataframe, 'number_of_rides')
                plot_metric_by_multiple_intervals(new_user_dataframe, 'zscore_percentile')
            else:
                plot_metric_by_multiple_intervals(new_user_dataframe, metric)
        keep_plotting = ask_user_if_more_metrics()
