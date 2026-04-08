# TSE Visualizer

A desktop Python application for exploring Tehran Stock Exchange (TSE) symbols with candlestick charts and Persian-friendly labels. It is designed as a simple but clear example of a local data-visualization workflow with GUI input, data retrieval, and chart generation.

## Key Features

- Tkinter desktop UI for symbol and date-range input
- Historical price retrieval via `finpy-tse`
- Candlestick + volume chart rendering with `mplfinance`
- Jalali-to-Gregorian date conversion for plotting
- Persian text reshaping support for chart labels
- Chart export to the `charts/` directory
- Basic click interaction: draw a line between two selected points on the chart

## Tech Stack

- **Language:** Python 3.10+
- **UI:** Tkinter
- **Data:** finpy-tse, pandas
- **Visualization:** matplotlib, mplfinance
- **Persian text/date utilities:** arabic-reshaper, python-bidi, jdatetime

## How It Works

1. User enters symbol + Jalali start/end dates (`YYYY-MM-DD`) in the GUI.
2. App fetches OHLCV history from `finpy-tse`.
3. Jalali index dates are converted to Gregorian dates for matplotlib compatibility.
4. Candlestick and volume chart are rendered.
5. Output image is saved to `charts/<symbol>_candlestick_chart_shamsi.png`.

## Installation

```bash
git clone <REPO_LINK>
cd tse-visualizer
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Then in the UI:
- Enter a TSE symbol (e.g., `فولاد`)
- Enter date range in Jalali format (`YYYY-MM-DD`)
- Click **Generate**

### Example Output

Generated charts are written to:

```text
charts/<SYMBOL>_candlestick_chart_shamsi.png
```

> You can add a screenshot to `docs/images/` and reference it here later.

## Project Structure

```text
.
├── main.py
├── requirements.txt
├── start_project.bat
├── tests/
│   └── test_plotting.py
└── tse_visualizer/
    ├── gui.py
    ├── plotting.py
    ├── stock_data.py
    └── utils.py
```

## Engineering Decisions

- **Lightweight desktop UX:** Tkinter keeps setup simple and dependency-light.
- **Separation of concerns:** data fetching, plotting, and GUI are split into dedicated modules.
- **Failure-safe defaults:** when the optional custom font is unavailable, a fallback font is used.
- **Output stability:** chart output directory is auto-created to avoid runtime save failures.

## Tests

Run unit tests with:

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## Future Improvements

- Add packaged releases (`pyinstaller`) for non-technical users
- Add date picker and symbol autocomplete in GUI
- Add richer error messages for network/API failures
- Add CI workflow (lint + tests) on pull requests

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
