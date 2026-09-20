from load_data import load_data
from clean_data import clean_data
from analyze_customers import identify_customers, create_customer_summary, create_high_value_customers, analyze_one_purchase_customers, analyze_product_concentration

def main():
    print("\nBEGIN\n")

    # LOAD
    df = load_data()
    print("\nLOADING DONE\n")

    print(df.head())
    print(df.shape)

    # CLEAN
    df = clean_data(df)
    print("\nCLEANING DONE\n")

    print(df.head())
    print(df.dtypes)

    if df is None:
        return
    
    # ANALYZE
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


    print("\nEND\n")

if __name__ == "__main__":
    main()