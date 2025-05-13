```python
import pandas as pd

# Load the uploaded file to examine its structure
file_path = '/mnt/data/assistant-HK6GQe63K29fBSKuRjnsps'
data = pd.read_csv(file_path)

# Display the first few rows of the dataset to understand its structure
data.head()
```

The dataset contains the following columns:

- **Country**: Name of the country.
- **ISO3 Code**: ISO3 code of the country.
- **Date**: Date of the electricity price record.
- **Price (EUR/MWhe)**: Electricity price in Euros per megawatt-hour.

To determine the country with the largest percentage change in electricity price over a single day, I will calculate the daily percentage change for each country and identify the maximum. Let me proceed.

```python
# Convert the 'Date' column to datetime format for easier manipulation
data['Date'] = pd.to_datetime(data['Date'])

# Sort the data by Country and Date to ensure proper calculation of daily changes
data = data.sort_values(by=['Country', 'Date'])

# Calculate the percentage change in price for each country
data['Price Change (%)'] = data.groupby('Country')['Price (EUR/MWhe)'].pct_change() * 100

# Find the maximum absolute percentage change and the corresponding country
max_change_row = data.loc[data['Price Change (%)'].abs().idxmax()]

max_change_row[['Country', 'Date', 'Price (EUR/MWhe)', 'Price Change (%)']]
```

The country with the largest percentage change in electricity price over a single day is **Austria**. On **April 13, 2015**, the electricity price experienced a massive percentage change of **29,987.5%**.
