# gets energy makeup from enstoe-e
# https://transparencyplatform.zendesk.com/hc/en-us/articles/12845911031188-How-to-get-security-token
from entsoe import EntsoePandasClient
import pandas as pd

API_TOKEN = 'YOUR_ENTSOE_TOKEN'

client = EntsoePandasClient(api_key=API_TOKEN)

# Define time window (must be timezone aware)
start = pd.Timestamp('2025-10-01 00:00', tz='Europe/Brussels')
end   = pd.Timestamp('2025-10-02 00:00', tz='Europe/Brussels')

# Query generation (all technologies) for Germany, for example
df = client.query_generation(country_code='DE', start=start, end=end)

print(df.head())
