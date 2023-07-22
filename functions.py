import json
import pandas as pd
from generate_plots import generate_plots

def filtering():
    df = pd.read_csv('product_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])

    with open('filters.json', 'r') as file:
        filters = json.load(file)

    if filters['product'] in df['Product'].unique():
        df = df[df['Product'] == filters['product']]

        # Daily frequency
        if filters['frequency'] == 'daily':
            selected_day = pd.to_datetime(filters['selected_day']).date()
            selected_day_str = selected_day.strftime('%Y-%m-%d')

            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
            if selected_day_str in df['Date'].values:
                df = df[df['Date'] == selected_day_str]
                generate_plots(df)
                return

                ##  Weekly frequency
        elif filters['frequency'] == 'weekly':
            selected_start_date = pd.to_datetime(filters['selected_start_date']).date()
            selected_start_date_str = selected_start_date.strftime('%Y-%m-%d')

            selected_end_date = pd.to_datetime(filters['selected_end_date']).date()
            selected_end_date_str = selected_end_date.strftime('%Y-%m-%d')

            df = df[(df['Date'] >= selected_start_date_str) & (df['Date'] <= selected_end_date_str)]
            generate_plots(df)
            return

            ## Monthly frequency
        elif filters['frequency'] == 'monthly':
            selected_month = pd.to_datetime(filters['selected_month'], format='%B').month
            df = df[df['Date'].dt.month == selected_month]
            generate_plots(df)
            return

            ## Yearly frequency
        elif filters['frequency'] == 'yearly':
            generate_plots(df)
            return

    else:
        print(
            f"Invalid product type: {filters['product']}. Available product types: {', '.join(df['Product'].unique())}")


def small_caps_to_title(word):
    if word:
        return word.capitalize()


def save_filters_to_json(product, frequency, selected_day=None, selected_start_date=None, selected_end_date=None,
                         selected_month=None):
    filters = {
        'product': product,
        'frequency': frequency,
        'selected_day': selected_day,
        'selected_start_date': selected_start_date,
        'selected_end_date': selected_end_date,
        'selected_month': selected_month
    }

    with open('filters.json', 'w') as file:
        json.dump(filters, file)



