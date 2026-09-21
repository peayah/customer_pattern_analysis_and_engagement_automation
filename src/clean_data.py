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
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

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