import matplotlib.pyplot as plt
import pandas as pd
from plotting.test_dictionary_pre_dataframe import test_dictionary_one, test_dictionary_two, test_dictionary_three, test_dictionary_four, test_dictionary_five, test_dictionary_six
from convert_to_dataframe import clean_convert_dictionary_to_dataframe
from user.dates import days_between_dates
from plotting.colors import assign_colors_to_dates
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from descriptors import descriptions_for_column_keys, graphable_columns, start_stations_to_zips

# https://matplotlib.org/stable/api/markers_api.html
# using the above link, choose the best markers
markers = ['D', '.', 'v', '^', 'p', '<', '>', '*', '1', '2', '3', '4']

# https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
# using the above link, choose standard linestyles
linestyles = [('solid', 'solid'),
     ('dotted', 'dotted'), 
     ('dashed', 'dashed'),   
     ('dashdot', 'dashdot'),  
     ('loosely dotted',        (0, (1, 10))),
     ('dotted',                (0, (1, 1))),
     ('densely dotted',        (0, (1, 1))),
     ('long dash with offset', (5, (10, 3))),
     ('loosely dashed',        (0, (5, 10))),
     ('dashed',                (0, (5, 5))),
     ('densely dashed',        (0, (5, 1))),

     ('loosely dashdotted',    (0, (3, 10, 1, 10))),
     ('dashdotted',            (0, (3, 5, 1, 5))),
     ('densely dashdotted',    (0, (3, 1, 1, 1))),

     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))]

# https://matplotlib.org/stable/gallery/color/named_colors.html
colors = list(mcolors.BASE_COLORS.keys()) + list(mcolors.TABLEAU_COLORS.keys())
# print(colors)

def match_format(current_dict, candidate_keys):
    """
    function which checks which item in a list is contained as a key in a dictionary
    used when a there are multiple items, each of which belong to different dictionaries
    this will match up the dictionary to the correct item
    
    input:
        current_dict: a dictionary which has as keys one of the list items in candidate_keys
        candidate_keys: a list of keys that may be found in current_dict

    output:
        key: the key that was found in the dictionary
    """
    for key in candidate_keys:
        if key in current_dict.keys():
            return key
    print("NO MATCH FOUND - ERROR")


def get_dates_without_year(interval_data_datetime):
    """
    take in a column on datetimes, return just the dates (without years) for each

    input:
        interval_data_datetime: pandas dataframe column containing datetimes
    
    output:
        dates: a list of dates without the year
    """
    dates = []
    for current_datetime in interval_data_datetime:
        # get the date by itself without the year
        datetime_without_year = current_datetime.split('-')[1] + '-' + current_datetime.split('-')[2]
        formatted_date_without_year = datetime.strptime(datetime_without_year, "%m-%d")
        dates.append(formatted_date_without_year)

    return dates


def get_unique_values(dataframe):
    """
    take in a dataframe, collect key unique sets to be returned to calling function

    input:
        dataframe: the dataframe
    
    output:
        unique_interval_columns: a dataframe containing only the unique zip codes and date ranges, with no other data
        unique_start_dates_with_year: unique YYYY-MM-DD found in the start_date column in the dataframe
        unique_start_dates_without_year: unique MM-DD found in the start_date column in the dataframe
        unique_zip_codes: unique NNNNN found in the zip_codes column in the dataframe
        unique_years: unique YYYY found in the start_date column in the dataframe
    """
    # collect various unique values
    unique_interval_columns = dataframe[['start_date', 'end_date', 'zip_code']].drop_duplicates()
    
    # collect unique start dates YYYY-MM-DD
    unique_start_dates_with_year = set(dataframe['start_date'].unique())
    
    # collect unique start dates MM-DD
    unique_start_dates_without_year = {date.split('-')[1] + '-' + date.split('-')[2] for date in unique_start_dates_with_year}
    
    # get unique zip codes NNNNN
    unique_zip_codes = set(dataframe['zip_code'].unique())
    
    # get unique years NNNNN
    unique_years = {date.split('-')[0] for date in unique_start_dates_with_year}
    
    return unique_interval_columns, unique_start_dates_with_year, unique_start_dates_without_year, unique_zip_codes, unique_years


def assign_differentiators(years, zips, starts):
    """
    the assummption made is that the following rankings hold true, from easiest to use to differentiate to hardest to use: color, line, marker
    it is also assumed that with multiple dates, it is easiest if dates are colors
    otherwise, assign largest set - easiest to differentiate

    input:
        years: set containing the years
        zips: set containig the zip codes
        starts: set containing start dates, without years (MM-DD)

    output: 
        color_set_string: the name of the set (ex. 'year') that is the color set
        line_set_string, marker_set_string: see above
        color_dict: the color dictionary, mapping items in the color_set to colors
        line_dict, marker_dict: see above

    """
    # if there is more than one date range, it is easiest to have it be color
    if len(starts) > 1:
        color_set_string = 'Date'
        color_set = starts

        # between years and zips, assign the line_set to the larger value
        if len(years) > len(zips):
            line_set_string = 'Year'
            line_set = years
            marker_set_string = 'Zip Code'
            marker_set = zips
        else:
            line_set_string = 'Zip Code'
            line_set = zips
            marker_set_string = 'Year'
            marker_set = years

        # create the color dictionary using assign_colors_to_dates
        color_dict = assign_colors_to_dates(starts)
    
    # if there is only one start date
    else:
        # let the marker set be the dates
        marker_set_string = 'Date'
        marker_set = starts

        # between years and zips, assign the color_set to the larger value
        if len(years) > len(zips):
            color_set_string = 'Year'
            color_set = years
            line_set_string = 'Zip Code'
            line_set = zips
        else:
            color_set_string = 'Zip Code'
            color_set = zips
            line_set_string = 'Year'
            line_set = years

        # create the color dictionary by using the colors list
        color_dict = {set_item: colors[i % len(color_set)] for i, set_item in enumerate(color_set)}
    
    # in both cases, generate line_dict and marker_dict
    line_dict = {set_item: linestyles[i % len(linestyles)][1] for i, set_item in enumerate(line_set)}
    marker_dict = {set_item: markers[i % len(markers)] for i, set_item in enumerate(marker_set)}
    return color_set_string, color_dict, line_set_string, line_dict, marker_set_string, marker_dict


def get_formatted_date_without_year(date_with_year):
    """
    take in unformatted date with year, return formatted date without year

    input:
        date_with_year: string in format YYYY-MM-DD

    output:
        formatted_date_without_year: datetime object in format MM-DD
    """
    date_without_year = date_with_year.split('-')[1] + '-' + date_with_year.split('-')[2]
    formatted_date_without_year = datetime.strptime(date_without_year, "%m-%d")
    return formatted_date_without_year


def plot_metric_by_single_interval(dataframe, metric):
    """
    given a dataframe containing one unique date interval and a single metric to be plotted, plot the graph
    since only one interval is being examined, the dates serve as the x-ticks

    input:
        dataframe: the dataframe
        metric: the metric chosen by user to be graphed

    output:
        matplotlib graph
    """
    # collect unique values
    unique_interval_columns, _, _, unique_zip_codes, unique_years = get_unique_values(dataframe)
    
    # determine color_dict and line_dict
    # marker dict is unneeded since only one start_date
    color_set_string, color_dict, line_set_string, line_dict, _, _ = assign_differentiators(unique_years, unique_zip_codes, set())
    
    # print(unique_interval_columns)
    # print(color_dict)

    start_date, end_date = None, None
    # iterate over the rows of the dataframe to plot intervals
    for _, interval in unique_interval_columns.iterrows():

        # access current start date, end date, zip code, and year
        start_date, end_date, zip_code = interval['start_date'], interval['end_date'], interval['zip_code']
        year = start_date.split('-')[0]

        # print(start_date)
        # print(end_date)
        # access the current data (full rows)
        interval_data = dataframe[(dataframe['start_date'] == start_date) & (dataframe['end_date'] == end_date) & (dataframe['zip_code'] == zip_code)]

        # determine which is the line key and which is the color key by matching format of keys
        line_key = match_format(line_dict, [year, zip_code])
        color_key = match_format(color_dict, [year, zip_code])

        # determine if the interval crosses january first, in which case the handling is slightly different
        formatted_start_date_without_year = get_formatted_date_without_year(start_date)
        formatted_end_date_without_year = get_formatted_date_without_year(end_date)
        crosses_jan_first = formatted_start_date_without_year > formatted_end_date_without_year

        if crosses_jan_first:
            # get dates for x-axis with year
            dates = interval_data['datetime']
            if len(line_dict) == 1:
                plt.plot(dates, interval_data[metric], color=color_dict[color_key], linestyle = line_dict[line_key])
            else:
                plt.plot(range(len(dates)), interval_data[metric], color=color_dict[color_key], linestyle = line_dict[line_key])
                min_metric_value = dataframe[metric].min()
                max_metric_value = dataframe[metric].max()
                # iterate through each day
                for x, current_datetime in zip(range(days_between_dates(start_date, end_date)), interval_data['datetime']):

                    # get the date by itself without the year
                    datetime_without_year = current_datetime.split('-')[1] + '-' + current_datetime.split('-')[2]

                    # plot the date and the label, use min_metric_value as the ceiling and keep moving down five units based on how many dates have already been plotted
                    plt.scatter(x, min_metric_value - (max_metric_value - min_metric_value) / 14, color='black', marker='o')
                    plt.text(x, min_metric_value - (max_metric_value - min_metric_value) / 14  + (max_metric_value - min_metric_value) / 70, datetime_without_year, fontsize=8, ha='center')
        else:
            dates = get_dates_without_year(interval_data['datetime'])

            plt.plot(dates, interval_data[metric], color=color_dict[color_key], linestyle = line_dict[line_key])

    # if length of line_dict is 1, include the line_dict value on the x-axis so it is easy to see
    # in this case, there is only one date range and zip provided, so there is only one line
    # however, if crosses_jan_first, we plot full dates so skip this
    if len(line_dict) == 1 and not crosses_jan_first:
        line_key = next(iter(line_dict.keys()))
        plt.xlabel(f'Date for {line_set_string} {line_key}')
    else:
        # date on the x-axis
        plt.xlabel("Date")
    
    plt.ylabel(descriptions_for_column_keys[metric])

    # add padding so that values are not hugging the y-axis or right edge of graph
    padding = timedelta(days=1)
    
    if crosses_jan_first:
        if len(line_dict) == 1:
            plt.xticks(dates)
        else:
            plt.xticks(range(len(dates)))

    else:
        # format dates as x-ticks
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
        plt.gcf().autofmt_xdate()
        plt.xlim(formatted_start_date_without_year - padding, formatted_end_date_without_year + padding)

    # only add line_dict to the legend if more than one item, otherwise it has already been put on x-axis title
    if len(line_dict) == 1:
        handles = [plt.Line2D([0], [0], color=color_item, label=set_item) for set_item, color_item in color_dict.items()]
        plt.legend(handles=handles, title=f'{color_set_string}')
    else:
        handles = [plt.Line2D([0], [0], marker = 'o', linestyle='', color=color_item, label=set_item) for set_item, color_item in color_dict.items()]
        handles += [plt.Line2D([0], [0], linestyle=linestyle, label=set_item, color = 'black') for set_item, linestyle in line_dict.items()]
        plt.legend(handles=handles, title='Zip Code / Year')

    plt.title(f'{descriptions_for_column_keys[metric]} vs Date', loc='center', fontsize=16, fontweight='bold')
    plt.show()


def plot_metric_by_multiple_intervals(dataframe, metric):
    """
    create a line for each interval / zip code pair. plot the line for a single metric against day # as days pass

    input:
        dataframe: the dataframe that contains the data
        metric: the metric to be plotted

    output: 
        matplotlib graph
    """
    # collect unique values
    unique_intervals_only, _, unique_start_dates_without_year, unique_zip_codes, unique_years = get_unique_values(dataframe)

    # determine color_dict and line_dict
    # marker dict is unneeded since only one start_date
    color_set_string, color_dict, line_set_string, line_dict, marker_set_string, marker_dict = assign_differentiators(unique_years, unique_zip_codes, unique_start_dates_without_year)

    # create an empty set to track which start dates have been plotted at the bottom of the graph
    start_dates_plotted = set()

    # find min, max value for purposes of ceiling / scale graphing date lines
    min_metric_value = dataframe[metric].min()
    max_metric_value = dataframe[metric].max()

    # iterate over the rows of the dataframe
    for _, interval in unique_intervals_only.iterrows():

        # access start date, end date, and zip code
        start_date, end_date, zip_code = interval['start_date'], interval['end_date'], interval['zip_code']

        # total number of days to graph
        days = days_between_dates(start_date, end_date) + 1

        # current year - key for lines dictionary
        year = start_date.split('-')[0]

        # current date without year - key for colors dictionary
        start_date_without_year = start_date.split('-')[1] + '-' + start_date.split('-')[2]

        # get keys for dictionaries
        color_key = start_date_without_year
        line_key = match_format(line_dict, [year, zip_code])
        marker_key = match_format(marker_dict, [year, zip_code])

        # access the data
        interval_full_data = dataframe[(dataframe['start_date'] == start_date) & (dataframe['end_date'] == end_date) & (dataframe['zip_code'] == zip_code)]

        # plot
        plt.plot(range(days), interval_full_data[metric], marker=marker_dict[marker_key], color=color_dict[color_key], linestyle = line_dict[line_key])

        # if the dot for that start date has not already been plotted
        if start_date_without_year not in start_dates_plotted:
            # add to the set
            start_dates_plotted.add(start_date_without_year)

            # iterate through each day
            for x, current_datetime in zip(range(days), interval_full_data['datetime']):

                # get the date by itself without the year
                datetime_without_year = current_datetime.split('-')[1] + '-' + current_datetime.split('-')[2]

                # plot the date and the label, use min_metric_value as the ceiling and keep moving down five units based on how many dates have already been plotted
                plt.scatter(x, min_metric_value - (max_metric_value - min_metric_value) / 14 * len(start_dates_plotted), color=color_dict[color_key], marker='o')
                plt.text(x, min_metric_value - (max_metric_value - min_metric_value) / 14 * len(start_dates_plotted) + (max_metric_value - min_metric_value) / 70, datetime_without_year, fontsize=8, ha='center')

    # if length of marker_dict is 1, include the marker_dict value on the x-axis so it is easy to see
    if len(marker_dict) == 1:
        marker_key = next(iter(marker_dict.keys()))
        plt.xlabel(f'Date for {marker_set_string} {marker_key}')
    else:
        plt.xlabel("Date")
    plt.ylabel(metric)
    
    days_in_interval = range(0, days_between_dates(dataframe['start_date'][0], dataframe['end_date'][0]) + 1)
    plt.xticks(days_in_interval)

    # only add marker_dict to the legend if more than one item, otherwise it has already been put on x-axis title
    if len(marker_dict) == 1:
        handles = [plt.Line2D([0], [0], linestyle=linestyle, label=set_item, color = 'black') for set_item, linestyle in line_dict.items()]
        plt.legend(handles=handles, title=f'{line_set_string}')
    else:
        handles = [plt.Line2D([0], [0], marker=marker, linestyle='', label=set_item, color = 'black') for set_item, marker in marker_dict.items()]
        handles += [plt.Line2D([0], [0], linestyle=linestyle, label=set_item, color = 'black') for set_item, linestyle in line_dict.items()]
        plt.legend(handles=handles, title='Zip Code / Year')

    plt.title(f'{descriptions_for_column_keys[metric]} vs Date', loc='center', fontsize=16, fontweight='bold')

    plt.show()


if __name__ == '__main__':
    test_dataframe_two = clean_convert_dictionary_to_dataframe(test_dictionary_two)
    plot_metric_by_single_interval(test_dataframe_two, 'temp')
    test_dataframe_three = clean_convert_dictionary_to_dataframe(test_dictionary_three)
    plot_metric_by_single_interval(test_dataframe_three, 'feelslikemax')
    test_dataframe_one = clean_convert_dictionary_to_dataframe(test_dictionary_one)
    plot_metric_by_multiple_intervals(test_dataframe_one, 'daylight')
    # test_dataframe_four = clean_convert_dictionary_to_dataframe(test_dictionary_four)
    # for metric in descriptions_for_column_keys.keys():
    #     if metric in graphable_columns:
    #         plot_metric_by_single_interval(test_dataframe_four, metric)
    # test_dataframe_five = clean_convert_dictionary_to_dataframe(test_dictionary_five)
    # plot_metric_by_single_interval(test_dataframe_five, 'daylight')
    # test_dataframe_six = clean_convert_dictionary_to_dataframe(test_dictionary_six)
    # plot_metric_by_single_interval(test_dataframe_six, 'daylight')