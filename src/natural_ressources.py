#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a single daily CSV (2015-01-01..2025-01-31) with:
- Brent crude (USD/bbl) -> BZ=F
- Dutch TTF gas (EUR/MWh) -> try TTF=F, then TTG=F (required)
- API2 coal (USD/t) -> MTF=F
Weekend/holiday rows are filled (ffill) and first day is backfilled once.

CLI:
  python fossil.py --out fuels_daily.csv --eur
  python fossil.py --start 2015-01-01 --end 2025-01-31 --no-fill
"""

import argparse, sys
import pandas as pd
import numpy as np
import yfinance as yf

def dl_series(ticker: str, start: str, end: str) -> pd.Series:
    df = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False, group_by="column")
    if df is None or df.empty:
        return pd.Series(dtype=float, name=ticker)
    # Prefer Adj Close; fall back to Close; handle potential MultiIndex columns
    if "Adj Close" in df.columns:
        s = df["Adj Close"]
    elif "Close" in df.columns:
        s = df["Close"]
    else:
        # Try to locate multi-index slice; else pick first numeric col
        try:
            s = df.xs("Adj Close", axis=1, level=0, drop_level=False)
        except Exception:
            try: s = df.xs("Close", axis=1, level=0, drop_level=False)
            except Exception: s = df.select_dtypes(include=[np.number]).iloc[:, :1]
    # squeeze to Series
    if isinstance(s, pd.DataFrame):
        s = s.iloc[:, 0]
    s.name = ticker
    return s

def first_ok(tickers, start, end, required=False, label=None):
    for t in tickers:
        s = dl_series(t, start, end)
        if not s.empty and s.notna().to_numpy().any():
            return t, s
    if required:
        raise SystemExit(f"ERROR: Could not fetch required series {label or ''} from tickers: {tickers}")
    return None, pd.Series(dtype=float)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", default="2015-01-01")
    ap.add_argument("--end",   default="2025-01-31")
    ap.add_argument("--out",   default="fuels_daily_2015_2025.csv")
    ap.add_argument("--eur",   action="store_true", help="Also add EUR-converted columns using EURUSD=X")
    ap.add_argument("--no-fill", action="store_true", help="Do NOT fill weekends/holidays (default is to fill)")
    ap.add_argument("--brent", default=None, help="Override Brent ticker (default BZ=F)")
    ap.add_argument("--ttf",   default=None, help="Override TTF ticker (default tries TTF=F then TTG=F)")
    ap.add_argument("--coal",  default=None, help="Override API2 coal ticker (default MTF=F)")
    args = ap.parse_args()

    start, end = args.start, args.end
    idx = pd.date_range(start, end, freq="D")

    # ---- Brent
    brent_list = [args.brent] if args.brent else ["BZ=F"]
    brent_tic, brent = first_ok(brent_list, start, end, required=False, label="Brent")
    if not brent.empty:
        brent.name = "brent_usd_bbl"

    # ---- TTF (REQUIRED) – try continuous + fallback
    ttf_list = [args.ttf] if args.ttf else ["TTF=F", "TTG=F"]
    ttf_tic, ttf = first_ok(ttf_list, start, end, required=True, label="TTF gas (EUR/MWh)")
    ttf.name = "ttf_eur_mwh"

    # ---- API2 coal
    coal_list = [args.coal] if args.coal else ["MTF=F"]
    coal_tic, coal = first_ok(coal_list, start, end, required=False, label="API2 coal")
    if not coal.empty:
        coal.name = "api2_usd_t"

    # ---- combine on daily calendar
    cols = [s for s in [brent, ttf, coal] if not s.empty]
    out = pd.concat(cols, axis=1).reindex(idx)
    out.index.name = "date"

    # Fill weekends/holidays by default
    if not args.no_fill:
        # Forward-fill, then one backfill to set the very first day if it was NaN
        out = out.ffill().bfill(limit=1)

    # Optional USD -> EUR conversion with EURUSD=X (USD per EUR)
    if args.eur:
        fx = dl_series("EURUSD=X", start, end).reindex(idx)
        if fx.notna().to_numpy().any():
            if "brent_usd_bbl" in out.columns:
                out["brent_eur_bbl"] = out["brent_usd_bbl"] / fx
            if "api2_usd_t" in out.columns:
                out["api2_eur_t"]   = out["api2_usd_t"] / fx
        else:
            print("WARNING: EURUSD=X unavailable; EUR conversion skipped.", file=sys.stderr)

    # Tidy column order
    order = [c for c in ["brent_usd_bbl","brent_eur_bbl","ttf_eur_mwh","api2_usd_t","api2_eur_t"] if c in out.columns]
    out = out[order]

    out.to_csv(args.out)
    used = {"Brent": brent_tic, "TTF": ttf_tic, "Coal": coal_tic, "FX": ("EURUSD=X" if args.eur else None)}
    print(f"Saved {args.out}")
    print("Tickers used:", {k:v for k,v in used.items() if v})

if __name__ == "__main__":
    main()
