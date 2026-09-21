import pandas as pd

def create_customer_summary(df):

    customer_summary = (
        df.groupby("CustomerID")
        .agg(
            Purchases=("InvoiceNo", "nunique"),
            Total_Spend=("Revenue", "sum"),
            Avg_Transaction=("Revenue", "mean"),
            Unique_Products=("StockCode", "nunique"),
        )
    )

    return customer_summary


def identify_customers(df):
    """
    separate records with an identified CustomerID from
    records with CustomerID 0.
    """

    identified = df[df["CustomerID"] != "0"].copy()

    return identified


def create_high_value_customers(customer_summary):
    """
    identify top 20% based on total spend.
    """

    top_20_count = round(len(customer_summary) * 0.20)

    high_value_customers = (
        customer_summary
        .sort_values("Total_Spend", ascending=False)
        .head(top_20_count)
        .copy()
    )

    other_customers = customer_summary.drop(
        high_value_customers.index
    ).copy()

    return high_value_customers, other_customers


def analyze_one_purchase_customers(customer_summary):
    """
    divide customers into those who made one purchase and those
    who made multiple purchases.
    """

    one_purchase_customers = customer_summary[
        customer_summary["Purchases"] == 1
    ].copy()

    multiple_purchase_customers = customer_summary[
        customer_summary["Purchases"] > 1
    ].copy()

    return one_purchase_customers, multiple_purchase_customers


def analyze_product_concentration(df):
    """
    analyze the number of unique products purchased by each customer.
    """

    product_concentration = (
        df.groupby("CustomerID")
        .agg(
            Purchases=("InvoiceNo", "nunique"),
            Total_Spend=("Revenue", "sum"),
            Unique_Products=("StockCode", "nunique"),
        )
        .sort_values("Unique_Products")
    )

    return product_concentration

def calculate_customer_rhythm(df):
    """
    Calculate each customer's typical purchasing interval
    and variation based on invoice-level purchases.
    """

    purchase_events = (
        df
        .groupby(["CustomerID", "InvoiceNo"])
        .agg(
            Purchase_Date=("InvoiceDate", "min")
        )
        .reset_index()
        .sort_values(["CustomerID", "Purchase_Date"])
    )

    purchase_events["Days_Between"] = (
        purchase_events
        .groupby("CustomerID")["Purchase_Date"]
        .diff()
        .dt.total_seconds()
        .div(86400)
    )

    # Ignore same-day purchases when establishing purchasing rhythm
    valid_intervals = purchase_events[
        purchase_events["Days_Between"] > 0
    ].copy()

    customer_rhythm = (
        valid_intervals
        .groupby("CustomerID")["Days_Between"]
        .agg(
            Typical_Interval="median",
            Average_Interval="mean",
            Interval_Variation="std",
            Interval_Count="count"
        )
    )

    return customer_rhythm


def calculate_customer_recency(df):
    """
    Calculate the number of days since each customer's
    most recent observed purchase.
    """

    last_purchase = (
        df
        .groupby("CustomerID")["InvoiceDate"]
        .max()
    )

    analysis_date = df["InvoiceDate"].max()

    recency = (
        analysis_date - last_purchase
    ).dt.total_seconds().div(86400)

    return recency.rename("Days_Since_Last_Purchase")
