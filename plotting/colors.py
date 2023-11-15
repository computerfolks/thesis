import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from datetime import datetime

def assign_colors_to_dates(date_set):
    """
    take in a set of unique dates, return a mapping of dates to colors over a gradient

    input:
        date_set: a set of unique dates without year
    
    output:
        color_dict: a dictionary with dates as keys (ex. '12-01') and colors as values (ex. (0.0, 1.0, 1.0, 1.0))
    """
    # put into a sorted list
    date_list = sorted(date_set, key=lambda x: datetime.strptime(x, '%m-%d'))

    # easily access min and max date using sorted list
    # collect in correct format
    min_date = datetime.strptime(date_list[0], '%m-%d')
    max_date = datetime.strptime(date_list[-1], '%m-%d')

    # https://matplotlib.org/stable/gallery/color/colormap_reference.html
    # gradient choice still TBD
    cmap = plt.cm.get_cmap('cool')

    # plot according to min being 0, max being days between min and max dates
    norm = mcolors.Normalize(vmin=0, vmax=(max_date - min_date).days)
    color_dict = {}

    # go through each date and find the color
    for date in date_list:
        date_obj = datetime.strptime(date, '%m-%d')

        # normalize on the gradient by finding days between min date and current date
        color_dict[date] = cmap(norm((date_obj - min_date).days))

    return color_dict

# testing
if __name__ == '__main__':
  dates = {'2021-01-01', '2023-01-01', '2023-02-01', '2023-03-01', '2023-10-01'}
  color_dict = assign_colors_to_dates(dates)

  # plot for testing, very basic
  for date, color in color_dict.items():
      plt.plot(date, 0, 'o', color=color)

  plt.show()
