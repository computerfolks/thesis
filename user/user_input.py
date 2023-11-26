import sys
sys.path.append(".")
from user.dates import collect_valid_start_and_end, days_between_dates, collect_valid_date, calc_end_date_from_start_date_and_interval_length, is_valid_date
from user.zips import collect_valid_zip_code_list
from descriptors import max_query_cost

def ask_user_if_more_intervals():
    """
    ask user if more intervals are meant to be added for analysis

    output:
        T/F
    """
    answer = input("To enter more intervals, type 'y' and press enter. Otherwise, type any other key and press enter: ")
    if answer.lower() == 'y':
        return True
    else:
        return False



def print_instruction_string_for_user_input():
    print(f"""
        Start by picking your first time interval (start date - end date) to explore.
        When you set the length of this date interval, all future intervals will be of the same length.

        For this time interval, you can provide a list of zip codes to include in the data report.
          
        Please note that your total number of (days * zip codes) must be less than {max_query_cost}.
        This is to reduce API costs. 
        For example, if you examine five zip codes and your time interval is 12 days, that would be a total of 60.

        Don't worry - the prompts will guide you as you input dates and zip codes.""")


def get_date_range_keys_zip_codes_values_dictionary():
    """
    Collects user input for date intervals and associated zip codes for data analysis. 
    Ensures the total query cost remains within the specified maximum query cost. 
    The function repeatedly prompts the user to input date intervals and associated zip codes. 
    It calculates the total cost of each query and checks if the addition of new queries exceeds the maximum cost. 
    The function returns a dictionary where the keys are tuples representing date ranges, and the values are lists of associated zip codes for each date interval.

    output:
        date_range_zip_codes_dict: A dictionary containing date intervals as keys and corresponding lists of zip codes as values.
    """
    print_instruction_string_for_user_input()

    # COLLECT FIRST INTERVAL
    # keep trying until the first interval is successfuly obtained
    successful_initial_date_interval = False
    while successful_initial_date_interval is False:
        # the total cost of all individual date ranges and zip code queries
        total_query_cost = 0

        # object to be returned, containing date ranges as keys and zip code list as values
        date_range_zip_codes_dict = {}
        
        # collect start and end date
        start_date, end_date = collect_valid_start_and_end()

        # collect zip code list, remove duplicates using set casting
        zip_code_list = list(set(collect_valid_zip_code_list()))

        # calculate the interval for this date range, and all future date ranges
        number_of_days_in_interval = days_between_dates(start_date, end_date) + 1

        # add to query cost the query cost of current request
        total_query_cost += number_of_days_in_interval * len(zip_code_list)
        print(f"Current query total cost {total_query_cost} out of {max_query_cost}")

        # if query cost exceeded, try again and inform user
        if total_query_cost > max_query_cost:
            print(f"Error: max query cost {max_query_cost} exceeded. Try again.")

        else:
            # save current data, move to next step because initial interval success
            date_range_zip_codes_dict[(start_date, end_date)] = zip_code_list
            successful_initial_date_interval = True

    # if max cost reached or would be reached with a single additional zip code, 
    # set more_intervals_desired to False to avoid asking user for more intervals
    if total_query_cost == max_query_cost or (max_query_cost - total_query_cost) < number_of_days_in_interval:
        print("Adding another zip code and date range to analyze would exceed max query cost - no more entries will be accepted")
        more_intervals_desired = False
    
    # otherwise, ask user if more intervals are desired
    else:
        more_intervals_desired = ask_user_if_more_intervals()



    # collect more intervals
    # loop while more intervals are desired and adding more intervals is possible without exceeding max query cost
    while(more_intervals_desired):
        print(f"Interval set to {number_of_days_in_interval} for all intervals.")

        # get valid start date
        start_date = collect_valid_date("start")

        # calculate end date based on start date and days in interval
        # will return None if end date is invalid (caused by start date being too late)
        end_date = calc_end_date_from_start_date_and_interval_length(start_date, number_of_days_in_interval - 1)
        if end_date is None:
            print(f"End date exceeds maximum date. Please enter an earlier start date.")
            continue
        print(f"End date calculated as {end_date}")

        # get zip code list
        zip_code_list = collect_valid_zip_code_list()

        # tally current query cost into total
        total_query_cost += number_of_days_in_interval * len(zip_code_list)   
        print(f"Current query total cost {total_query_cost} out of {max_query_cost}")

        # if max has been exceeded, inform user of current total and ask if they want more, dropping current data
        if total_query_cost > max_query_cost:
            print(f"Error: max query cost {max_query_cost} exceeded. Current interval will be ignored.")
            total_query_cost -= number_of_days_in_interval * len(zip_code_list)
            print(f"Current query total cost {total_query_cost} out of {max_query_cost}")
            more_intervals_desired = ask_user_if_more_intervals()
            continue


        # add current data to dictionary

        # if date has already been seen, add new zips to existing list
        if (start_date, end_date) in date_range_zip_codes_dict.keys():
            current_zip_list = date_range_zip_codes_dict[(start_date, end_date)]

            for zip_code in zip_code_list:

                # avoid adding duplicates
                if zip_code in current_zip_list:
                    print(f"{zip_code} already requested for date range {start_date}, {end_date} and will be ignored")
                    total_query_cost -= number_of_days_in_interval
                    print(f"Current query total cost {total_query_cost} out of {max_query_cost}")
                
                else:
                    current_zip_list.append(zip_code)
            
            date_range_zip_codes_dict[(start_date, end_date)] = current_zip_list
        
        else:
            date_range_zip_codes_dict[(start_date, end_date)] = zip_code_list

        # if max cost reached or would be reached with a single additional zip code, break
        if (max_query_cost - total_query_cost) < number_of_days_in_interval:
            print("Adding another zip code and date range to analyze would exceed max query cost - no more entries will be accepted")
            break

        # ask user if more intervals are desired
        more_intervals_desired = ask_user_if_more_intervals()

    return date_range_zip_codes_dict


# testing
if __name__ == '__main__':
    test_result = get_date_range_keys_zip_codes_values_dictionary()
    print(test_result)


