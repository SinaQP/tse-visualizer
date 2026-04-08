"""Data access layer for Tehran Stock Exchange historical prices."""

from __future__ import annotations

import pandas as pd
import finpy_tse as tse


REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def fetch_stock_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """Fetch OHLCV price history for a symbol in Jalali date format.

    Args:
        symbol: TSE symbol (for example: "فولاد").
        start_date: Jalali start date formatted as YYYY-MM-DD.
        end_date: Jalali end date formatted as YYYY-MM-DD.

    Returns:
        A DataFrame indexed by Jalali date strings. Returns an empty DataFrame when
        data is unavailable or the upstream request fails.
    """
    try:
        stock_data = tse.Get_Price_History(
            symbol, start_date=start_date, end_date=end_date
        )
    except Exception:
        return pd.DataFrame()

    if stock_data is None or stock_data.empty:
        return pd.DataFrame()

    available_columns = [col for col in REQUIRED_COLUMNS if col in stock_data.columns]
    return stock_data[available_columns] if available_columns else stock_data
