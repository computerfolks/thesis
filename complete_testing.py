from user.user_input import get_date_range_keys_zip_codes_values_dictionary
from query import get_query_results_for_date_range_zip_codes_dict
from convert_to_dataframe import clean_convert_dictionary_to_dataframe
from plotting.plot_one_metric import plot_metric_by_multiple_intervals, plot_metric_by_single_interval, get_formatted_date_without_year
from plotting.test_dictionary_pre_dataframe import test_dictionary_seven
from descriptors import start_stations_to_zips, graphable_columns


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
    columns_to_choose = graphable_columns
    if bike_rides_available:
        columns_to_choose.append('bikerides')

    valid_column = False
    while valid_column is False:
        print("Enter the metric you would like to plot. You must choose from the following list: ")
        print(graphable_columns)
        column = input()
        if column in graphable_columns:
            return column
        else:
            print(f"{column} not found in list. Please try again.")

def ask_user_if_more_metrics():
    """
    ask user if more metrics should be graphed, or if user wants program to exit

    output:
        T/F
    """
    answer = input("To graph more metrics, type 'y' and press enter. Otherwise, type any other key and press enter: ")
    if answer.lower() == 'y':
        return True
    else:
        return False

# collect user_dict of zip codes and intervals
user_dict = get_date_range_keys_zip_codes_values_dictionary()
# print(user_dict)

# query for weather data
new_user_query_results = get_query_results_for_date_range_zip_codes_dict(user_dict)
# print(new_user_query_results)

# convert to dataframe
new_user_dataframe = clean_convert_dictionary_to_dataframe(new_user_query_results)

# determine if there is one interval of MM-DD or not
one_interval = has_one_interval(user_dict)

# collect unique zip codes
zips = extract_zips(user_dict)

# determine if bike_ride data is available (only true if all zips have been trained on)
bike_ride = bike_rides_available(zips)

# if bike ride is available, I need to somehow incorporate that into the dataframe. 
# Best method is likely to print z-score converted to % and just print that 50% is average day
if bike_ride:
    pass

# plot as long as user wants more metrics plotted
keep_plotting = True
while(keep_plotting):
    metric = metric_to_plot(bike_ride)
    if one_interval:
        plot_metric_by_single_interval(new_user_dataframe, metric)
    else:
        plot_metric_by_multiple_intervals(new_user_dataframe, metric)
    keep_plotting = ask_user_if_more_metrics()
