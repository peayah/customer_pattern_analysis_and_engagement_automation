import sys

sys.path.append(
    "/Users/peayah/Desktop/piasmithcom_projects/customer_pattern_analysis_and_engagement_automation"
)

import pandas as pd

from src.load_data import load_data
from src.clean_data import clean_data
from src.analyze_customers import (
    identify_customers,
    create_customer_summary,
    create_high_value_customers,
)
from src.determine_state import determine_customer_state

def test_customer_states():

    df = load_data("online_retail.csv")
    df = clean_data(df)

    df["CustomerID"] = df["CustomerID"].astype(str)

    expected = pd.read_csv(
        "data/customer_state_test.csv",
        dtype={"CustomerID": str}
    )

    test_ids = expected["CustomerID"].tolist()

    test_df = df[
        df["CustomerID"].isin(test_ids)
    ].copy()

    results = determine_customer_state(test_df)

    comparison = expected.merge(
        results[["CustomerID", "State"]],
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