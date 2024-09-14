import pandas as pd
import mplfinance as mpf
import jdatetime
import matplotlib.pyplot as plt
from tse_visualizer.utils import reshape_persian_text, load_font
from tse_visualizer.stock_data import fetch_stock_data

def plot_candlestick_chart(symbol, start_date, end_date):
    stock_data = fetch_stock_data(symbol, start_date, end_date)

    if stock_data.empty:
        print("No data found.")
        return

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

    # Interactive line drawing
    lines = []

    def on_click(event):
        if event.inaxes == axlist[0]:  # Ensure the click is within the main candlestick chart
            lines.append((event.xdata, event.ydata))
            if len(lines) == 2:
                x_values, y_values = zip(*lines)
                axlist[0].plot(x_values, y_values, color='blue')
                fig.canvas.draw()
                lines.clear()

    fig.canvas.mpl_connect('button_press_event', on_click)

    plt.savefig(f'charts/{symbol}_candlestick_chart_shamsi.png')
    plt.show()
