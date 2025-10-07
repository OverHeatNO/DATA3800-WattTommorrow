# Gets closing price electricity for Euro countries 
<<<<<<< HEAD
import pandas as pd
import matplotlib.pyplot as plt
import os
import kagglehub
# ✅ CORRECT line using the relative path from the 'src' directory
df = pd.read_csv('content/european_wholesale_electricity_price_data_monthly.csv')

df['Date'] = pd.to_datetime(df['Date'])
# Create a table with Date as index and countries as columns
df_pivot = df.pivot(index='Date', columns='Country', values='Price (EUR/MWhe)')

selected_countries = ['Germany', 'France', 'Italy', 'Spain', 'Belgium']
plt.figure(figsize=(12,6))

for country in selected_countries:
    plt.plot(df_pivot.index, df_pivot[country], label=country, linewidth=2)

plt.xlabel('Date')
plt.ylabel('Price (EUR/MWhe)')
plt.title('Electricity Prices Over Time')
plt.legend()
plt.grid(True)
plt.show()
=======

print("test")
>>>>>>> a3719a9bd2d353eedbf0f89dff9211cbbcf67f35
