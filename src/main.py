from load_data import load_data
from clean_data import clean_data
from analyze_customers import (
    identify_customers, 
    create_customer_summary, 
    create_high_value_customers, 
    analyze_one_purchase_customers, 
    analyze_product_concentration,
)
from analyze_products import (
    analyze_product_duration,
    analyze_zero_day_products,
    analyze_product_reach,
    analyze_zero_day_revenue,
    analyze_high_value_zero_day_participation,
)
def main():
    print("\nBEGIN\n")
    ###################
    # LOAD
    df = load_data()
    print("\nLOADING DONE\n")

    print(df.head())
    print(df.shape)
    ###################
    # CLEAN
    df = clean_data(df)
    print("\nCLEANING DONE\n")

    print(df.head())
    print(df.dtypes)
    ###################
    if df is None:
        return
   ###################
    # ANALYZE CUSTOMERS
    identified = identify_customers(df)

    customer_summary = create_customer_summary(identified)

    high_value_customers, other_customers = (
        create_high_value_customers(customer_summary)
    )

    one_purchase_customers, multiple_purchase_customers = (
        analyze_one_purchase_customers(customer_summary)
    )

    product_concentration = analyze_product_concentration(identified)

    print(customer_summary.head())
    print("\nCUSTOMER ANALYSIS DONE\n")
    ###################
    # ANALYZE CUSTOMERS

    product_date_range = analyze_product_duration(identified)

    zero_day_products, zero_day_stock_codes = (
        analyze_zero_day_products(
            identified,
            product_date_range
        )
    )

    product_reach = analyze_product_reach(
        identified,
        zero_day_stock_codes
    )

    zero_day_revenue = analyze_zero_day_revenue(
        identified,
        zero_day_stock_codes
    )

    high_value_zero_day_participation = (
        analyze_high_value_zero_day_participation(
            identified,
            zero_day_stock_codes,
            high_value_customers
        )
    )

    print(product_date_range.head())
    print(zero_day_products.head())
    print(product_reach.head())
    print(f"Zero-day revenue: ${zero_day_revenue:,.2f}")
    print(high_value_zero_day_participation)

    print("\nPRODUCT ANALYSIS DONE\n")

    ###################
    #  
    
    
    
    
    
    
    ###################
    print("\nEND\n")

if __name__ == "__main__":
    main()