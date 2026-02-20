# smart_pipeline.py - Data processing WITH inline learning
# Same test: 50 CSV files - 3 failures (6% failure rate) = 91% improvement

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

# HEY CLAUDE: Remember the encoding crashes on user-uploaded files?
# MISTAKE: pd.read_csv() with no encoding crashed on files saved from Excel
# LESSON: Excel exports CSV as cp1252 on Windows, not UTF-8
# LESSON: Files from different countries/systems use different encodings
# RULE: Always try UTF-8 first, catch UnicodeDecodeError and retry with latin-1


def process_sales_data(csv_file):

    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        log.warning('UTF-8 failed - retrying with latin-1 encoding')
        df = pd.read_csv(csv_file, encoding='latin-1')

    # HEY CLAUDE: Remember the KeyError crashes on column access?
    # MISTAKE: Assumed column names match exactly - crashed when source had
    #          'Date' vs 'date' or 'sale_price' vs 'price'
    # LESSON: Real CSV files have inconsistent headers from different systems
    # RULE: Always validate required columns exist before any processing
    required = ['date', 'price', 'quantity']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f'Missing required columns: {missing}. Found: {list(df.columns)}')

    # HEY CLAUDE: Remember the date parsing failures on international files?
    # MISTAKE: pd.to_datetime(df['date']) crashed on dates like "27-Dec-2024"
    # LESSON: Date formats vary by country - MM/DD/YYYY vs DD/MM/YYYY vs ISO
    # RULE: Always use errors='coerce' so bad dates become NaT not exceptions
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    bad_dates = df['date'].isna().sum()
    if bad_dates > 0:
        log.warning(f'{bad_dates} rows have unparseable dates - set to NaT')

    # HEY CLAUDE: Remember the silent NaN revenue rows?
    # MISTAKE: price * quantity = NaN when either value is missing
    # LESSON: pandas NaN arithmetic propagates silently - no error, wrong totals
    # RULE: Fill NaN with 0 before arithmetic OR drop rows - document the choice
    # CONTEXT: Business rule here is missing price/quantity = no revenue counted
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
    df['revenue'] = df['price'] * df['quantity']

    # Data quality report - useful for stakeholders
    negative = (df['revenue'] < 0).sum()
    zero = (df['revenue'] == 0).sum()

    if negative > 0:
        log.warning(f'{negative} rows have negative revenue - check source data')

    summary = {
        'total_revenue': round(df['revenue'].sum(), 2),
        'avg_order': round(df['revenue'].mean(), 2),
        'num_orders': len(df),
        'data_quality': {
            'unparseable_dates': int(bad_dates),
            'negative_revenue_rows': int(negative),
            'zero_revenue_rows': int(zero),
        }
    }

    return summary


if __name__ == '__main__':
    try:
        result = process_sales_data('sales_data.csv')
        print(f"Total Revenue:  ${result['total_revenue']:,.2f}")
        print(f"Average Order:  ${result['avg_order']:,.2f}")
        print(f"Order Count:    {result['num_orders']}")
        print(f"Data Quality:   {result['data_quality']}")
    except Exception as e:
        print(f'Error: {e}')
