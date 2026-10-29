
from load_data import load_data
from clean_data import clean_data
from find_zero_day_products import find_zero_day_products


def test_find_zero_day_products():

    df = load_data("retail_data.csv")
    df = clean_data(df)

    identified = df[
        df["CustomerID"] != "0"
    ].copy()

    zero_day_products = find_zero_day_products(
        identified
    )

    # Results should not be empty
    assert not zero_day_products.empty

    # Required columns should exist
    expected_columns = [
        "StockCode",
        "Min_Date",
        "Max_Date",
        "Description",
        "Days_Active",
    ]

    assert all(
        column in zero_day_products.columns
        for column in expected_columns
    )

    # Every returned product should have zero days active
    assert zero_day_products["Days_Active"].eq(0).all()

    # Earliest timestamp should not exceed latest timestamp
    assert (
        zero_day_products["Min_Date"]
        <= zero_day_products["Max_Date"]
    ).all()

    print(
        f"\nZero-day products identified: "
        f"{len(zero_day_products)}"
    )


if __name__ == "__main__":
    test_find_zero_day_products()