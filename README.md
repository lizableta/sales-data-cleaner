# Sales Data Cleaner

## About the Project

This is a small Python project I made to practise working with sales data using Pandas. The original data contains missing values, duplicate rows, inconsistent text, different date formats, and values stored in the wrong format.

The program checks and cleans the data, calculates summary statistics, and saves the results without changing the original files.

## Requirements

- Python 3.10 or newer
- Pandas

## Project Structure

- `data/` — contains the original CSV and JSON files.
- `output/` — contains the cleaned data and summary.
- `cleaner.py` — contains the functions for loading, cleaning, and summarizing data.
- `main.py` — runs the cleaning process and exports the results.
- `check_data.py` — helps inspect the original data.
- `requirements.txt` — lists the required Python library.

## How to Run the Project

Open a terminal in the project folder.

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate it

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the project using the virtual environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

### 3. Install the required library

```bash
python -m pip install -r requirements.txt
```

### 4. Run the program

```bash
python main.py
```

To use the JSON file instead, change the `input_file` value in `main.py` to `data/sales_raw.json`.

To inspect the original data before cleaning, run:

```bash
python check_data.py
```

## What the Program Does

- Standardizes column names.
- Replaces empty or whitespace-only values with missing values.
- Removes exact duplicate rows.
- Standardizes city, category, product, and status names.
- Converts supported date formats into a consistent date format.
- Converts quantity and unit price into numeric values.
- Marks invalid dates, unknown quantities, and negative quantities or prices as missing.
- Calculates sales totals and other summary statistics.
- Exports the cleaned data and summary.

## Cleaning Decisions

I removed exact duplicate rows but kept records that share an order ID when their other details are different. These records might represent different items or transactions, so I did not automatically delete them.

I changed `five` to `5` and treated `unknown` as a missing quantity. I treated `free` as a price of zero, based on the assumption that it means the item was free.

Negative quantities, negative prices, and invalid dates are marked as missing instead of deleting the entire record. Fractional quantities, such as `2.5`, are treated as missing because this dataset counts whole products. Negative quantities and negative prices are also treated as missing instead of rounding them or deleting the entire record.

Missing values are not automatically replaced with zero, because doing so could produce misleading results.

The program calculates total sales for all statuses and separately for completed records. These calculations use records that have both a valid quantity and a valid unit price. The summary also reports how many records have the information needed for these calculations.

## Output

After running the program, two files are created in the `output/` folder:

- `sales_cleaned.csv` — the cleaned sales data.
- `sales_summary.json` — summary statistics, including row counts, missing values, duplicate counts, sales totals, and records by category and status.

The original data files are not changed.