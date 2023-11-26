"""
This file is used to make the API call
"""

import urllib.request
import json

# visual crossing api link
base_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'

# get api key which is not uploaded because it is in a .gitignore
with open('api_key.txt', 'r') as file:
  api_key = file.read().strip()

def query_builder(start_date, end_date, zip_code, units = 'us'):
    """
    construct query for api call, return string containing the api call link

    input:
      zip_code: valid US zip
      start_date: first date in the range of dates to collect data
      end_date: end date in the range of dates to collect data
      units: which system of units to use, options include ['us', 'uk', 'metric', 'base']

    output:
      url: api url

    possible future functionality:
    include: list of sections to include in query response, 'days' by default to exclude hourly data
    elements: list of subset of weather elements to collect - if None, collect all
    """

    # build query
    url = base_url + str(zip_code) + '/' + start_date + '/' + end_date + '/' + "?key=" + api_key + "&include=days" 
    return url

def query_attempt(url):
    """
    function which attempts to make an api call to the 'url' for the weather data and returns the raw result
    """
    print(f"Running query URL: {url}")
    
    # get response, load it into JSON
    response = urllib.request.urlopen(url)
    data = response.read()
    raw_data = json.loads(data.decode('utf-8'))

    return raw_data


def get_query_result_for_date_range_zip_code(start_date, end_date, zip_code):
  """
  get complete query results for a given start_date, end_date, zip_code

  input:
    start_date, end_date: dates in correct format, representing the range to query
    zip_code: valid US zip code

  output:
    a tuple with two values
    the first value is a tuple of the input to the function
    the second value is the raw_result from the api call

  """

  # construct the query
  query = query_builder(start_date, end_date, zip_code)

  # get raw result
  raw_result = query_attempt(query)

  return (start_date, end_date, zip_code), raw_result


def get_query_results_for_date_range_zip_codes_dict(date_range_zip_codes_dict):
  """
  given dictionary containing:
    as keys: tuples of date ranges
    as values: the list of zip codes for the date range
  query and return query result for each date range - zip code pair, and return with format of dictionary with key : value as
  start_date, end_date, zip_code : query_result

  input: 
    date_range_zip_codes_dict: ex. ('2012-01-01', '2012-01-03'): ['11516', '11559', '11598']

  output:
    total_results: dictionary with query results organized by start_date, end_date, and zip_code
  """

  # store all the results
  total_results = {}

  # loop through date intervals
  for start_date, end_date in date_range_zip_codes_dict.keys():

    # loop through each zip code for the given date interval
    for zip_code in date_range_zip_codes_dict[(start_date, end_date)]:
      
      # collect return values from function
      current_key, current_result = get_query_result_for_date_range_zip_code(start_date, end_date, zip_code)

      # store in dictionary
      total_results[current_key] = current_result
  
  return total_results



# testing
if __name__ == '__main__':
    test_dict = {('2022-12-30', '2023-1-5'): ['11559', '33433'], ('2021-12-30', '2022-01-05'): ['11559', '33433'], ('2023-6-10', '2023-06-16'): ['11559']}
    print(get_query_results_for_date_range_zip_codes_dict(test_dict))