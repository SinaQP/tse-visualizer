import finpy_tse as tse

def fetch_stock_data(symbol, start_date, end_date):
    try:
        stock_data = tse.Get_Price_History(symbol, start_date=start_date, end_date=end_date)
        return stock_data
    except Exception as e:
        print(f"مشکلی در دریافت اطلاعات وجود دارد: {e}")
        return pd.DataFrame()