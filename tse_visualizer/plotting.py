"""Chart rendering utilities."""

from __future__ import annotations

from pathlib import Path

import jdatetime
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

from tse_visualizer.stock_data import fetch_stock_data
from tse_visualizer.utils import ensure_directory, load_font, reshape_persian_text


def convert_jalali_index_to_gregorian(index: pd.Index) -> pd.DatetimeIndex:
    """Convert Jalali date strings (YYYY-MM-DD) to Gregorian DatetimeIndex."""
    return pd.to_datetime(
        pd.Series(index).apply(
            lambda date: jdatetime.date(*map(int, str(date).split("-")))
            .togregorian()
            .strftime("%Y-%m-%d")
        )
    )


def plot_candlestick_chart(
    symbol: str,
    start_date: str,
    end_date: str,
    output_dir: str | Path = "charts",
) -> Path | None:
    """Render and save a candlestick chart for a TSE symbol.

    Returns the saved image path, or None when there is no data to plot.
    """
    stock_data = fetch_stock_data(symbol, start_date, end_date)
    if stock_data.empty:
        return None

    stock_data.index = convert_jalali_index_to_gregorian(stock_data.index)
    font_prop = load_font()

    fig, axes = mpf.plot(
        stock_data,
        type="candle",
        style="charles",
        title=reshape_persian_text(f"نمودار کندلی {symbol}"),
        ylabel=reshape_persian_text("قیمت"),
        ylabel_lower=reshape_persian_text("حجم"),
        volume=True,
        returnfig=True,
    )

    chart_axis = axes[0]
    step = max(1, len(stock_data) // 10)
    tick_positions = range(0, len(stock_data), step)

    chart_axis.set_xticks(tick_positions)
    chart_axis.set_xticklabels(
        [
            reshape_persian_text(
                jdatetime.date.fromgregorian(date=greg_date).strftime("%Y-%m-%d")
            )
            for greg_date in stock_data.index[::step]
        ],
        rotation=45,
    )
    chart_axis.set_xlabel(reshape_persian_text("تاریخ"), fontproperties=font_prop)

    # Simple interaction: draw a segment between every two clicks.
    click_points: list[tuple[float, float]] = []

    def on_click(event):
        if event.inaxes != chart_axis:
            return
        click_points.append((event.xdata, event.ydata))
        if len(click_points) == 2:
            x_values, y_values = zip(*click_points)
            chart_axis.plot(x_values, y_values, color="blue")
            fig.canvas.draw()
            click_points.clear()

    fig.canvas.mpl_connect("button_press_event", on_click)

    chart_dir = ensure_directory(output_dir)
    output_path = chart_dir / f"{symbol}_candlestick_chart_shamsi.png"
    plt.savefig(output_path, bbox_inches="tight")
    plt.show()
    return output_path
