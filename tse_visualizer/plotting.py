import pandas as pd
import mplfinance as mpf
import jdatetime
import matplotlib.pyplot as plt
from tse_visualizer.utils import reshape_persian_text, load_font
from tse_visualizer.stock_data import fetch_stock_data

def plot_candlestick_chart(symbol, start_date, end_date, shapes_data=None):
    stock_data = fetch_stock_data(symbol, start_date, end_date)

    if stock_data.empty:
        print("No data found.")
        return

    # Convert Shamsi dates to Gregorian
    gregorian_index = pd.to_datetime(stock_data.index.to_series().apply(
        lambda date: jdatetime.date(*map(int, date.split('-'))).togregorian().strftime('%Y-%m-%d')
    ))

    stock_data.index = gregorian_index

    font_prop = load_font()

    fig, axlist = mpf.plot(stock_data, type='candle', style='charles',
                           title=reshape_persian_text(f'نمودار کندلی {symbol}'),
                           ylabel=reshape_persian_text('قیمت'),
                           ylabel_lower=reshape_persian_text('حجم'),
                           volume=True,
                           returnfig=True)

    axlist[0].set_xticks(range(0, len(stock_data), max(1, len(stock_data)//10)))
    axlist[0].set_xticklabels(
        [reshape_persian_text(jdatetime.date.fromgregorian(date=greg_date).strftime('%Y-%m-%d'))
         for greg_date in gregorian_index[::max(1, len(stock_data)//10)]],
        rotation=45
    )

    axlist[0].set_xlabel(reshape_persian_text('تاریخ'), fontproperties=font_prop)

    # Drawing shapes on the chart if provided
    if shapes_data:
        print('here')
        draw_shapes_on_chart(shapes_data, axlist[0], gregorian_index)

    plt.savefig(f'charts/{symbol}_candlestick_chart_shamsi.png')
    plt.show()


import pandas as pd
from bisect import bisect_left


def find_nearest_date(date_str, available_dates):
    """ Find the nearest date to the given date_str in available_dates. """
    available_dates = pd.to_datetime(available_dates)
    target_date = pd.to_datetime(date_str)
    pos = bisect_left(available_dates, target_date)

    if pos == 0:
        return available_dates[0]
    if pos == len(available_dates):
        return available_dates[-1]

    before = available_dates[pos - 1]
    after = available_dates[pos]
    return after if after - target_date < target_date - before else before


def draw_shapes_on_chart(shapes_data, ax, gregorian_dates):
    # Convert gregorian_dates (which is a pandas Series) to a list of strings in 'YYYY-MM-DD' format
    gregorian_index = gregorian_dates.dt.strftime('%Y-%m-%d').tolist()

    print("Gregorian dates in stock data:", gregorian_index)  # Log the available dates in the stock data

    for shape in shapes_data:
        # Convert Shamsi (Jalali) dates to Gregorian
        start_date_shamsi = shape['start_point']['date']
        end_date_shamsi = shape['end_point']['date']

        # Convert Shamsi to Gregorian
        start_date_gregorian = jdatetime.date(*map(int, start_date_shamsi.split('-'))).togregorian()
        end_date_gregorian = jdatetime.date(*map(int, end_date_shamsi.split('-'))).togregorian()

        print(f"Shamsi Start: {start_date_shamsi}, Gregorian Start: {start_date_gregorian}")
        print(f"Shamsi End: {end_date_shamsi}, Gregorian End: {end_date_gregorian}")

        # Convert to string format for comparison
        start_date_str = start_date_gregorian.strftime('%Y-%m-%d')
        end_date_str = end_date_gregorian.strftime('%Y-%m-%d')

        # Find the nearest available dates in the stock data
        nearest_start_date = find_nearest_date(start_date_str, gregorian_index)
        nearest_end_date = find_nearest_date(end_date_str, gregorian_index)

        print(f"Nearest available start date: {nearest_start_date}")
        print(f"Nearest available end date: {nearest_end_date}")

        # Find the index for the start and end dates
        start_index = gregorian_index.index(nearest_start_date.strftime('%Y-%m-%d'))
        end_index = gregorian_index.index(nearest_end_date.strftime('%Y-%m-%d'))

        print(f"Start Index: {start_index}, End Index: {end_index}")

        # For debugging, plot markers at the start and end points
        ax.plot(start_index, shape['start_point']['price'], marker='o', color='red', label="Start Point")
        ax.plot(end_index, shape['end_point']['price'], marker='o', color='blue', label="End Point")

        # Drawing the shapes based on the shape type
        if shape['shape_type'] == 'line':
            print(
                f"Drawing line from {start_index} to {end_index} at prices {shape['start_point']['price']} to {shape['end_point']['price']}")
            ax.plot([start_index, end_index],
                    [shape['start_point']['price'], shape['end_point']['price']],
                    color=shape['color'], linestyle='-', linewidth=2)

        elif shape['shape_type'] == 'rectangle':
            print(
                f"Drawing rectangle from {start_index} to {end_index} at prices {shape['start_point']['price']} to {shape['end_point']['price']}")
            rect = plt.Rectangle((start_index, shape['start_point']['price']),
                                 end_index - start_index,
                                 shape['end_point']['price'] - shape['start_point']['price'],
                                 color=shape['color'], fill=False)
            ax.add_patch(rect)

        elif shape['shape_type'] == 'circle':
            radius = (end_index - start_index) / 2
            print(f"Drawing circle with center at {(start_index + end_index) / 2} and radius {radius}")
            circle = plt.Circle(
                ((start_index + end_index) / 2, (shape['start_point']['price'] + shape['end_point']['price']) / 2),
                radius, color=shape['color'], fill=False)
            ax.add_patch(circle)

        else:
            print(f"Unknown shape type: {shape['shape_type']}")
