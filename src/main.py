from load_data import load_data
from clean_data import clean_data

def main():
    print("\nBEGIN\n")
    df = load_data()

    print(df.head())
    print(df.shape)

    df = clean_data(df)

    print(df.head())
    print(df.dtypes)

    print("\nEND\n")

if __name__ == "__main__":
    main()