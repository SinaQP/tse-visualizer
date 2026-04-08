"""Tkinter GUI for querying and visualizing TSE candlestick charts."""

from __future__ import annotations

import re
import tkinter as tk
from tkinter import messagebox, ttk

from tse_visualizer.plotting import plot_candlestick_chart

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _is_valid_jalali_date_format(date_text: str) -> bool:
    return bool(DATE_PATTERN.match(date_text))


def on_submit(symbol_entry: ttk.Entry, start_date_entry: ttk.Entry, end_date_entry: ttk.Entry) -> None:
    symbol = symbol_entry.get().strip().upper()
    start_date = start_date_entry.get().strip()
    end_date = end_date_entry.get().strip()

    if not all([symbol, start_date, end_date]):
        messagebox.showwarning("Input error", "Please complete all fields.")
        return

    if not _is_valid_jalali_date_format(start_date) or not _is_valid_jalali_date_format(end_date):
        messagebox.showwarning("Invalid date", "Dates must use the YYYY-MM-DD format.")
        return

    output_path = plot_candlestick_chart(symbol, start_date, end_date)
    if output_path is None:
        messagebox.showinfo("No data", "No data found for the selected symbol/date range.")
    else:
        messagebox.showinfo("Chart generated", f"Chart saved to: {output_path}")


def create_main_window() -> tk.Tk:
    root = tk.Tk()
    root.title("TSE Visualizer")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="Symbol:").grid(row=0, column=1, sticky=tk.W)
    symbol_entry = ttk.Entry(frame, width=20)
    symbol_entry.grid(row=0, column=0)
    symbol_entry.insert(0, "فولاد")

    ttk.Label(frame, text="Start date (YYYY-MM-DD):").grid(row=1, column=1, sticky=tk.W)
    start_date_entry = ttk.Entry(frame, width=20)
    start_date_entry.grid(row=1, column=0)
    start_date_entry.insert(0, "1401-01-01")

    ttk.Label(frame, text="End date (YYYY-MM-DD):").grid(row=2, column=1, sticky=tk.W)
    end_date_entry = ttk.Entry(frame, width=20)
    end_date_entry.grid(row=2, column=0)
    end_date_entry.insert(0, "1401-02-20")

    ttk.Button(
        frame,
        text="Generate",
        command=lambda: on_submit(symbol_entry, start_date_entry, end_date_entry),
    ).grid(row=3, column=0, columnspan=2, pady=10)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    return root
