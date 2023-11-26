"""
This file is used to convert raw API output into a usable dataframe
"""

import pandas as pd
from plotting.test_dictionary_pre_dataframe import test_dictionary_one

def convert_dictionary_to_dataframe(total_dictionary_results):
    """
    converts a dictionary of results into a pandas DataFrame, where each row is a single date for a given location within the date range.

    input:
        total_dictionary_results = {
            ('start_date', 'end_date', 'zip_code'): {
                'queryCost': 3,
                'latitude': 40.627386,
                'longitude': -73.72852,
                'resolvedAddress': '11516, USA',
                'address': '11516',
                'timezone': 'America/New_York',
                'tzoffset': -5.0,
                'days': [
                    {
                        'datetime': '2012-01-01',
                        'datetimeEpoch': 1325394000,
                        'tempmax': 50.1,
                        'tempmin': 38.2,
                        # more key-value pairs
                    },
                    # additional dictionaries for each day
                ],
                'stations': { ... }
            },
        # additional entries with the same structure
        }

    output:
        dataframe: A Pandas DataFrame containing the results from the dictionary, where each row stores a single location/date pair. The date range can be easily determined, since the start_date and end_date are stored as values for each row.
    """
    # initialize dataframe variable
    dataframe = None

    # loop through each (start_date, end_date, zip_code)
    for interval_location in total_dictionary_results.keys():

        # access the values in the key
        start_date, end_date, zip_code = interval_location

        # access the dictionary containing the individual days in the date range for the location
        interval_location_dictionary = total_dictionary_results[interval_location]['days']

        # loop through each individual date
        for day_dictionary in interval_location_dictionary:

            # initialize dataframe with column names if have not done so already
            if dataframe is None:
                columns = ['start_date', 'end_date', 'zip_code'] + list(day_dictionary.keys())
                dataframe = pd.DataFrame(columns=columns)
            
            # include start_date, end_date, and zip_code
            row_values = [start_date, end_date, zip_code] 

            # include all other values in the dictionary, but only attempt to access from columns[3:] onwards to skip over start_date, end_date, zip_code
            row_values.extend([day_dictionary[column] if column in day_dictionary else None for column in dataframe.columns[3:]])

            # save row values
            dataframe.loc[len(dataframe)] = row_values

    return dataframe


def clean_convert_dictionary_to_dataframe(total_dictionary_results):
    """
    call convert_dictionary_to_dataframe, clean up output to add daylight and remove extra columns listed in columns_to_drop
    """
    raw_dataframe = convert_dictionary_to_dataframe(total_dictionary_results)

    # create daylight column
    raw_dataframe['daylight'] = raw_dataframe['sunsetEpoch'] - raw_dataframe['sunriseEpoch']
    
    # list columns to drop
    columns_to_drop = ['datetimeEpoch', 'sunriseEpoch', 'sunsetEpoch', 'conditions', 'description', 'icon', 'stations', 'source', 'precipprob', 'preciptype']
    
    # create new dataframe with dropped columns
    clean_dataframe = raw_dataframe.drop(columns=columns_to_drop, errors='ignore')

    return clean_dataframe


# testing
if __name__ == '__main__':

    # load testing dictionary
    total_dictionary_results = test_dictionary_one

    # test raw function
    print(convert_dictionary_to_dataframe(total_dictionary_results))

    # test clean function
    print("\n\n\n\n\n\n\n\nCLEAN")
    print(clean_convert_dictionary_to_dataframe(total_dictionary_results))