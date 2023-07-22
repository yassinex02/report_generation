import pandas as pd
import random
from datetime import datetime, timedelta

product_values = ['PB1', 'PB2']

maillon_values = ['Extraction', 'Manutention', 'Lavage']

start_date = datetime(2022, 7, 1)
end_date = datetime(2023, 7, 1)
date_range = pd.date_range(start_date, end_date - timedelta(days=1), freq='D')

df = pd.DataFrame(columns=['Product', 'Date', 'Teneur PBL', 'Humidite', 'Chlore', 'Maillon'])

for date in date_range:
    product = random.choice(product_values)
    teneur_pbl = random.uniform(0, 1)
    humidite = random.uniform(0, 1)
    chlore = random.uniform(0, 1)
    maillon = random.choice(maillon_values)
    df = df.append({
        'Product': product,
        'Date': date,
        'Teneur PBL': teneur_pbl,
        'Humidite': humidite,
        'Chlore': chlore,
        'Maillon': maillon
    }, ignore_index=True)

df.to_csv('product_data.csv', index=False)
