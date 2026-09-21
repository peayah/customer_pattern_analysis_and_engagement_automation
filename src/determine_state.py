import pandas as pd
import numpy as np

from analyze_customers import (
    identify_customers,
    create_customer_summary,
    calculate_customer_rhythm,
    calculate_customer_recency,
    identify_corporate_candidates,
)


def determine_customer_state(df):
    """
    Determine each customer's current behavioral state.

    States:
    - Insufficient History
    - Normal
    - Late
    - High-Value Late
    """

    # Identify customers
    identified = identify_customers(df)

    # Create customer-level summary
    customer_summary = create_customer_summary(
        identified
    )

    # Calculate purchasing rhythm
    rhythm = calculate_customer_rhythm(
        identified
    )

    # Calculate recency
    recency = calculate_customer_recency(
        identified
    )

    # Combine customer metrics
    customer_state = customer_summary.copy()

    customer_state = customer_state.join(rhythm)
    customer_state = customer_state.join(recency)

    # Identify high-value customers
    corporate_candidates = identify_corporate_candidates(
    customer_summary
    )

    corporate_ids = set(
    corporate_candidates.index
    )
    
    customer_state["Customer_Type"] = np.where(
        customer_state.index.isin(corporate_ids),
        "Corporate Candidate",
        "Other"
    )

    # Calculate how far the customer is beyond
    # their typical purchasing interval
    customer_state["Late_Ratio"] = (
        customer_state["Days_Since_Last_Purchase"]
        / customer_state["Typical_Interval"]
    )

    
    def assign_state(row):

        # Cannot establish a personal purchasing rhythm
        # with fewer than two observed purchases.
        if row["Purchases"] < 2:
            return "Insufficient History"

        # Cannot establish a usable rhythm
        # if there are no positive intervals.
        if pd.isna(row["Typical_Interval"]):
            return "Insufficient History"

        # 25% or more beyond the customer's typical interval
        # is considered meaningfully late.
        if row["Late_Ratio"] >= 1.25:

            if row["Customer_Type"] == "Corporate Candidate":
                return "High-Value Late"

            return "Late"

        return "Normal"

    customer_state["State"] = (
        customer_state
        .apply(assign_state, axis=1)
    )

    return customer_state