import pandas as pd


def create_product_date_range(df):
    """
    Create one row per product showing its first and
    last observed sale date.
    """

    product_date_range = (
        df
        .groupby("StockCode", dropna=False)
        .agg(
            Min_Date=("InvoiceDate", "min"),
            Max_Date=("InvoiceDate", "max"),
            Description=("Description", "first"),
        )
        .reset_index()
    )

    product_date_range["Days_Active"] = (
        product_date_range["Max_Date"]
        - product_date_range["Min_Date"]
    ).dt.days

    return product_date_range


def find_zero_day_products(df):
    """
    Identify products whose first and last observed
    sale date are the same day.
    """

    product_date_range = create_product_date_range(df)

    zero_day_products = product_date_range[
        product_date_range["Days_Active"] == 0
    ].copy()

    return zero_day_products