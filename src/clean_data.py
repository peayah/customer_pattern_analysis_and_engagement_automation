import pandas as pd


def clean_data(df):

    # Data types
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    df["CustomerID"] = (
        df["CustomerID"]
        .fillna(0)
        .astype(int)
        .astype(str)
    )

    # add revenue column
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]

    return df