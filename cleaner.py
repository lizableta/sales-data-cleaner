
import pandas as pd
from pathlib import Path


REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "customer",
    "city",
    "category",
    "product",
    "quantity",
    "unit_price",
    "status",
]


def load_data(file_path):
    """Load sales data from a CSV or JSON file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path, dtype=str)
    elif path.suffix.lower() == ".json":
        df = pd.read_json(path, dtype=False)
        df = df.astype({col: str for col in df.select_dtypes(
            include="object"
        ).columns})
    else:
        raise ValueError("Unsupported file format. Use CSV or JSON.")

    return df


def clean_data(df):
    """Clean sales data and return a cleaned copy."""
    df = df.copy()

    # Standardize column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )

    # Check that all required columns exist
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    # Treat empty or whitespace-only strings as missing
    df = df.replace(r"^\s*$", pd.NA, regex=True)

    # Remove exact duplicate rows only
    df = df.drop_duplicates().copy()

    # Clean text values
    text_columns = ["customer", "city", "category", "product", "status"]

    for column in text_columns:
        df[column] = df[column].str.strip()

    # Standardize capitalization
    df["city"] = df["city"].str.title()
    df["category"] = df["category"].str.title()
    df["product"] = df["product"].str.title()

    # Standardize status names
    df["status"] = df["status"].str.title()
    df["status"] = df["status"].replace({
        "Canceled": "Cancelled",
        "Complete": "Completed",
    })

    # Clean dates using the formats found in the dataset
    original_dates = df["order_date"].str.strip()

    date_formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
    ]

    cleaned_dates = pd.Series(
        pd.NaT,
        index=df.index,
        dtype="datetime64[ns]",
    )

    for date_format in date_formats:
        parsed_dates = pd.to_datetime(
            original_dates,
            format=date_format,
            errors="coerce",
        )
        cleaned_dates = cleaned_dates.fillna(parsed_dates)

    df["order_date"] = cleaned_dates

    # Clean quantity
    quantity = df["quantity"].str.strip().str.lower()
    quantity = quantity.replace({
        "five": "5",
        "unknown": pd.NA,
    })

    df["quantity"] = pd.to_numeric(quantity, errors="coerce")

    # Decimal and negative quantities are invalid for whole products
    df.loc[df["quantity"] % 1 != 0, "quantity"] = pd.NA
    df.loc[df["quantity"] < 0, "quantity"] = pd.NA

    # Use nullable integers so missing quantities are allowed
    df["quantity"] = df["quantity"].astype("Int64")

    # Clean unit price
    # Assumption: "free" means a price of zero
    unit_price = df["unit_price"].str.strip().str.lower()
    unit_price = unit_price.replace("free", "0")

    df["unit_price"] = pd.to_numeric(unit_price, errors="coerce")

    # Negative prices are treated as invalid
    df.loc[df["unit_price"] < 0, "unit_price"] = pd.NA

    return df


def create_summary(df, original_df):
    """Create summary metrics for the sales data."""

    # Count blank strings as missing values
    original_for_missing = original_df.replace(
        r"^\s*$", pd.NA, regex=True
    )

    cleaned_for_missing = df.replace(
        r"^\s*$", pd.NA, regex=True
    )

    # Count unique order IDs that appear more than once
    repeated_orders = df.loc[
        df["order_id"].duplicated(keep=False),
        "order_id",
    ].nunique()

    # Find records with valid revenue data
    valid_revenue_rows = (
        df["quantity"].notna() & df["unit_price"].notna()
    )

    completed_revenue_rows = (
        (df["status"] == "Completed") & valid_revenue_rows
    )

    # Calculate revenue for valid records
    all_sales = (
        df.loc[valid_revenue_rows, "quantity"]
        * df.loc[valid_revenue_rows, "unit_price"]
    ).sum()

    completed_sales = (
        df.loc[completed_revenue_rows, "quantity"]
        * df.loc[completed_revenue_rows, "unit_price"]
    ).sum()

    return {
        "rows_before_cleaning": int(len(original_df)),
        "rows_after_cleaning": int(len(df)),
        "exact_duplicate_rows_removed": int(
            original_df.duplicated().sum()
        ),
        "rows_removed": int(len(original_df) - len(df)),

        "missing_values_before": {
            column: int(count)
            for column, count
            in original_for_missing.isnull().sum().items()
        },
        "missing_values_after": {
            column: int(count)
            for column, count
            in cleaned_for_missing.isnull().sum().items()
        },

        "duplicate_rows_before": int(original_df.duplicated().sum()),
        "duplicate_rows_after": int(df.duplicated().sum()),

        "unique_orders": int(df["order_id"].nunique()),
        "repeated_order_ids": int(repeated_orders),

        "records_with_valid_revenue_data": int(valid_revenue_rows.sum()),
        "completed_records_with_valid_revenue_data": int(
            completed_revenue_rows.sum()
        ),

        "total_sales_all_statuses": round(float(all_sales), 2),
        "total_sales_completed_only": round(float(completed_sales), 2),

        "total_quantity_all_statuses": int(df["quantity"].sum()),
        "average_unit_price": round(float(df["unit_price"].mean()), 2),
        "unique_customers": int(df["customer"].nunique()),

        "records_by_category": {
            str(category): int(count)
            for category, count in df["category"].value_counts().items()
        },
        "records_by_status": {
            str(status): int(count)
            for status, count in df["status"].value_counts().items()
        },
    }
