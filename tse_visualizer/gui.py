import tkinter as tk
from tkinter import ttk, messagebox
from tse_visualizer.plotting import plot_candlestick_chart

def on_submit(symbol_entry, start_date_entry, end_date_entry):
    symbol = symbol_entry.get().strip().upper()
    start_date = start_date_entry.get().strip()
    end_date = end_date_entry.get().strip()

    if not all([symbol, start_date, end_date]):
        messagebox.showwarning("خطا در ورودی ها", "لطفا تمامی فیلد ها را کامل کنید")
        return

    plot_candlestick_chart(symbol, start_date, end_date)

def create_main_window():
    root = tk.Tk()
    root.title("TSE Visualizer")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="نماد:").grid(row=0, column=1, sticky=tk.W)
    symbol_entry = ttk.Entry(frame, width=20)
    symbol_entry.grid(row=0, column=0)
    symbol_entry.insert(0, "فولاد")  # Default value

    ttk.Label(frame, text="تاریخ شروع (YYYY-MM-DD):").grid(row=1, column=1, sticky=tk.W)
    start_date_entry = ttk.Entry(frame, width=20)
    start_date_entry.grid(row=1, column=0)
    start_date_entry.insert(0, "1401-01-01")  # Default value

    ttk.Label(frame, text="تاریخ پایان (YYYY-MM-DD):").grid(row=2, column=1, sticky=tk.W)
    end_date_entry = ttk.Entry(frame, width=20)
    end_date_entry.grid(row=2, column=0)
    end_date_entry.insert(0, "1401-02-20")  # Default value

    ttk.Button(frame, text="ثبت", command=lambda: on_submit(symbol_entry, start_date_entry, end_date_entry)).grid(row=3, column=0, columnspan=2, pady=10)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    return root
