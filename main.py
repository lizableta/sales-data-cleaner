
import json
from pathlib import Path

from cleaner import load_data, clean_data, create_summary


def main():
    # Choose the input file
    input_file = "data/sales_raw.csv"
    # You can change this to "data/sales_raw.json"

    output_folder = Path("output")
    output_folder.mkdir(parents=True, exist_ok=True)

    try:
        # Load the original data
        df = load_data(input_file)

        # Clean the data
        cleaned_df = clean_data(df)

        # Create summary statistics
        summary = create_summary(cleaned_df, df)

        # Export cleaned data
        cleaned_df.to_csv(
            output_folder / "sales_cleaned.csv",
            index=False,
        )

        # Export summary as JSON
        with open(
            output_folder / "sales_summary.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                summary,
                file,
                indent=4,
                ensure_ascii=False,
            )

        print("Cleaning completed!")
        print("Original rows:", len(df))
        print("Cleaned rows:", len(cleaned_df))
        print("Rows removed:", summary["rows_removed"])

        print("\nMissing values after cleaning:")
        print(cleaned_df.isnull().sum())

        print("\nSummary:")
        print(json.dumps(summary, indent=4, ensure_ascii=False))

    except (FileNotFoundError, ValueError, OSError) as error:
        print("The program could not finish:", error)


if __name__ == "__main__":
    main()
