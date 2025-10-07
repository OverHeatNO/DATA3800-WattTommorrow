# pip/conda: meteostat>=1.6, pandas>=1.3.6
from meteostat import Stations, Daily
from datetime import datetime
import pandas as pd

start = datetime(2015, 1, 1)
end   = datetime(2025, 1, 31)

def country_daily(country_code: str, n_stations: int = 200) -> pd.DataFrame:
    # 1) Pick stations in the country (correct API)
    st = Stations().region(country_code)  # e.g., 'NO' or 'FR'

    # 2) Keep only stations with daily records overlapping our period
    st = st.inventory('daily', (start, end))

    # 3) Grab up to N stations (increase if you want broader coverage)
    stations = st.fetch(n_stations)

    if stations.empty:
        raise RuntimeError(f"No stations with daily data found for {country_code} in {start:%Y-%m-%d}–{end:%Y-%m-%d}")

    ids = stations.index.tolist()

    # 4) Download daily data for those stations
    df = Daily(ids, start, end).fetch()

    # 5) Aggregate across stations → national daily median (robust to outliers/gaps)
    out = (
        df.reset_index()
          .groupby('time')
          .median(numeric_only=True)
          .sort_index()
    )
    out.index.name = "date"
    return out

no_daily = country_daily('NO')  # Norway
fr_daily = country_daily('FR')  # France

no_daily.to_csv("norway_meteostat_daily_2015_2025.csv")
fr_daily.to_csv("france_meteostat_daily_2015_2025.csv")
