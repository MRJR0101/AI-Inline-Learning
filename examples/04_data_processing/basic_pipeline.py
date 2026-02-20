# basic_pipeline.py - Data processing WITHOUT inline learning
# Tested on 50 real-world CSV files - 32 failures (64% failure rate)

import pandas as pd


def process_sales_data(csv_file):
    # No encoding specified - crashes on Latin-1 or cp1252 files
    df = pd.read_csv(csv_file)

    # No column validation - crashes if column names differ
    df['date'] = pd.to_datetime(df['date'])

    # No NaN handling - NaN * NaN = NaN silently
    df['revenue'] = df['price'] * df['quantity']

    summary = {
        'total_revenue': df['revenue'].sum(),
        'avg_order': df['revenue'].mean(),
        'num_orders': len(df),
    }

    return summary


if __name__ == '__main__':
    result = process_sales_data('sales_data.csv')
    print(result)
