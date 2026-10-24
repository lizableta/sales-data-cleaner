
import pandas as pd


file_path = "data/sales_raw.csv"

try:
    df = pd.read_csv(file_path, dtype=str)

    print("FIRST 5 ROWS")
    print(df.head())

    print("\nDATASET SIZE")
    print("Total rows:", len(df))
    print("Total columns:", len(df.columns))
    print("Column names:", list(df.columns))

    print("\nMISSING VALUES")
    print(df.replace(r"^\s*$", pd.NA, regex=True).isnull().sum())

    print("\nEXACT DUPLICATE ROWS")
    print(df.duplicated().sum())

    print("\nDATA TYPES")
    print(df.dtypes)

    print("\nUNIQUE PRODUCT NAMES")
    print(df["product"].unique())

    print("\nUNIQUE STATUSES")
    print(df["status"].unique())

    print("\nUNIQUE QUANTITY VALUES")
    print(df["quantity"].unique())

    print("\nUNIQUE UNIT PRICES")
    print(df["unit_price"].unique())

    print("\nDATES CONTAINING A SLASH")
    print(
        df.loc[
            df["order_date"].str.contains("/", na=False),
            "order_date",
        ].unique()
    )

    print("\nMOST COMMON ORIGINAL DATE VALUES")
    print(df["order_date"].value_counts(dropna=False).head(20))

    # Check repeated order IDs without assuming they are duplicates
    repeated = df[
        df["order_id"].duplicated(keep=False)
    ].sort_values("order_id")

    print("\nREPEATED ORDER IDs")
    print(repeated)

    print("\nNUMBER OF UNIQUE REPEATED ORDER IDs")
    print(repeated["order_id"].nunique())

    print("\nEXAMPLES OF REPEATED IDs WITH DIFFERENT DETAILS")
    different_details = (
        repeated.groupby("order_id")
        .filter(lambda group: len(group.drop_duplicates()) > 1)
    )

    print(different_details.head(10))

except FileNotFoundError:
    print(f"File not found: {file_path}")

except KeyError as error:
    print("A required column was not found:", error)
