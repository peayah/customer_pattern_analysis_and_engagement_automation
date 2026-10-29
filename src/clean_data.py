import pandas as pd

REQUIRED_COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
]

def clean_data(df):

     # check required columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        print("missing required columns:")
        for column in missing_columns:
            print(f"- {column}")

        return None

    print("\nrequired columns. Check\n")

    # remove duplicate rows
    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:
        print(f"\n{duplicate_count} duplicate rows. Investigate\n")
    else:
        print("no duplicate rows. Check")


    # data types
    # convert InvoiceDate to datetime
    # df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    ####
    date_strings = df["InvoiceDate"].astype("string").str.strip()

    parsed_dates = pd.to_datetime(
        date_strings,
        format="%m/%d/%y %H:%M",
        errors="coerce"
    )

    invalid_dates = parsed_dates.isna()
    invalid_count = invalid_dates.sum()
    invalid_percentage = (
        invalid_count / len(df) * 100 if len(df) > 0 else 0
    )

    print(f"Invalid dates: {invalid_count}")
    print(f"Invalid date percentage: {invalid_percentage:.2f}%")

    if invalid_percentage < 5:
        df = df.loc[~invalid_dates].copy()
        df["InvoiceDate"] = parsed_dates.loc[~invalid_dates]
        print(f"Removed {invalid_count} rows with invalid dates.")
    else:
        raise ValueError(
            f"{invalid_percentage:.2f}% of dates are invalid. "
            "This meets or exceeds the 5% threshold. "
            "Investigate the data before proceeding."
        )
    ####

    # add revenue column
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    # Sort by InvoiceDate
    df = df.sort_values("InvoiceDate").reset_index(drop=True)

    df["CustomerID"] = (
    df["CustomerID"]
    .astype(str)
    .str.replace(".0", "", regex=False)
    )

    return df