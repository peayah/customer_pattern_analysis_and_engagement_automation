import pandas as pd

from load_data import load_data
from clean_data import clean_data

from determine_state import determine_customer_state

def test_customer_states():

    df = load_data("retail_data.csv")
    df = clean_data(df)

    expected = pd.read_csv(
        "data/state_test_data.csv",
        dtype={"CustomerID": str}
    )

    test_ids = expected["CustomerID"].tolist()

    test_df = df[
        df["CustomerID"].isin(test_ids)
    ].copy()


    results = determine_customer_state(test_df)

    comparison = expected.merge(
    results[["State"]].reset_index(),
    on="CustomerID",
    how="left"
    )

    comparison["Test_Result"] = (
        comparison["Expected_State"]
        == comparison["State"]
    )

    print(comparison)


if __name__ == "__main__":
    test_customer_states()
    