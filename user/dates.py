from datetime import datetime, date, timedelta

def ask_user_for_date(start_or_end):
    """
    prompt the user for a start/end date, return input

    input:
        start_or_end: a string of value "start" or "end", used to prompt the user

    output:
        date: raw input provided by the user
    """
    raw_date_string = input(f"Please enter {start_or_end} date in format YYYY-MM-DD: ")
    return raw_date_string


def is_valid_date(raw_date_string):
    """
    ensure that a string is in correct format and is valid
    to be valid, a date must be between Jan. 1 1975 and present day + 14 days
    max_date is 14 days ahead, since that is the limit of some metrics being predicted

    input:
        raw_date_string: string to be examined
    
    output:
        T/F
    """
    date_format = "%Y-%m-%d"
    try:
        input_date = datetime.strptime(raw_date_string, date_format).date()
        present_date = date.today()

        # max_date is 14 days ahead, since that is the limit of some metrics being predicted
        max_date = date.today() + timedelta(days=14)

        # set date before which we do not have ability to query for results
        min_date = date(1975, 1, 1)

        # validate input_date
        if min_date <= input_date <= max_date:
            return True
        else:
            print(f"Error: Date should be between {min_date} and {max_date}.")
            return False
    
    # exception, including incorrect format
    except Exception as e:
        print(f"Error: {e}")
        return False
    

def collect_valid_date(start_or_end):
    """
    call on other functions, return valid date

    input:
        start_or_end: a string of value "start" or "end", used to prompt the user

    output:
        valid_date: a valid date
    """
    raw_date_string = ask_user_for_date(start_or_end)

    # while the date is invalid, keep asking user
    while is_valid_date(raw_date_string) is False:
        raw_date_string = ask_user_for_date(start_or_end)

    valid_date = raw_date_string
    return valid_date


def days_between_dates(date1, date2):
    """
    determine number of days between two dates

    input:
        date1, date2: two valid dates
    
    output:
        number of days between the dates
    """
    date_format = "%Y-%m-%d"

    try:
        # get datetime objects so that subtraction can be done without parsing
        date1_obj = datetime.strptime(date1, date_format)
        date2_obj = datetime.strptime(date2, date_format)

        # absolute value so that order the dates come in is irrelevant
        return abs((date2_obj - date1_obj).days)
    
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def is_valid_start_and_end_dates_pair(start_valid_date, end_valid_date):
    """
    verify that the pair of start date and end date are valid together
    to be valid together, the dates must be in the correct order chronologically
    and also cannot be more than max_query_cost apart (global parameter)

    input:
        start_valid_date, end_valid_date: valid dates
    
    output:
        T/F
    """
    if start_valid_date >= end_valid_date:
        print(f"Error: start date {start_valid_date} occurs after end date {end_valid_date}")
        return False
    
    else:
        days_difference = days_between_dates(start_valid_date, end_valid_date)

        # days_difference returns None when it throws an exception
        if days_difference is not None:
            return True
        else:
            return False


def collect_valid_start_and_end():
    """
    return valid start and end dates by calling other functions

    output:
        start_valid_date, end_valid_date: valid dates which are also valid together
    """
    print("You will be asked to enter the start and end dates.")
    
    # get valid start date and valid end date - collect_valid_date ensures the dates are valid on their own
    start_valid_date = collect_valid_date("start")
    end_valid_date = collect_valid_date("end")
    
    # while the dates are not valid together as a pair
    while is_valid_start_and_end_dates_pair(start_valid_date, end_valid_date) is False:
        print("You will now be re-prompted to enter dates")
        start_valid_date = collect_valid_date("start")
        end_valid_date = collect_valid_date("end")
    
    # return the dates, which are now verified to be a valid pair with each other
    return start_valid_date, end_valid_date


def calc_end_date_from_start_date_and_interval_length(start_date, number_of_days_in_interval):
    """
    function which calculates the end date based on the start date and number of days to add

    input:
        start_date: starting date in correct format
        number_of_days_in_interval: number of days between start and end dates

    output:
        end_date
    """
    date_format = "%Y-%m-%d"
    try:
        start_date_obj = datetime.strptime(start_date, date_format)
        end_date_obj = start_date_obj + timedelta(days=number_of_days_in_interval)
        return end_date_obj.strftime(date_format)
    except ValueError as e:
        print(f"Error: {e}")
        return None