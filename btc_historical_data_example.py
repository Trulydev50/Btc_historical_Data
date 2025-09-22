import json
import requests as rq
import pandas as pd
import openpyxl
from pathlib import Path


PUB_DEMO_URL = "https://api.coingecko.com/api/v3"
PUB_PRO_URL = "https://pro-api.coingecko.com/api/v3"


def get_Demo_key():
    # CHANGE the path if your file is elsewhere
    with open(r"YOUR_KEYS_FILE_PATH", "r", encoding="utf-8") as f:
        key_dict = json.load(f)
    # Adjust the key name to match your JSON 
    return key_dict.get("x-cg-demo-api-key")


def get_Pro_key():
    # CHANGE the path if your file is elsewhere
    with open(r"YOUR_KEYS_FILE_PATH", "r", encoding="utf-8") as f:
        key_dict = json.load(f)
    # Adjust the key name to match your JSON 
    return key_dict.get("x-cg-pro-api-key")


def get_Response(endpoint, headers=None, params=None, base_url=None):
    url = f"{base_url}{endpoint}"
    #print(f"[DEBUG] GET {url} params={params}")  # <-- forces visible output
    resp = rq.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data
key = get_Demo_key()
headers = {"accept": "application/json", "x-cg-demo-api-key": key}
base_url = PUB_DEMO_URL
params = {"vs_currency": "usd", "days": "7", "interval": "daily"} #parameters to query upon, BTC daily data for the past 7 days
mc = get_Response("/coins/bitcoin/market_chart", headers=headers, params=params, base_url=base_url )

#Shape the data
def series_to_df(series, value_col):
    df = pd.DataFrame(series, columns=["ts_ms", value_col])
    df["date"] = pd.to_datetime(df["ts_ms"], unit="ms")
    return df[["date", value_col]]


df_price  = series_to_df(mc.get("prices", []),        "price_usd")
df_mcap   = series_to_df(mc.get("market_caps", []),   "market_cap_usd")
df_volume = series_to_df(mc.get("total_volumes", []), "volume_24h_usd")


df = (
    df_price.merge(df_mcap, on="date", how="left")
            .merge(df_volume, on="date", how="left")
            .sort_values("date")
            .reset_index(drop=True)
)[["date", "price_usd", "market_cap_usd", "volume_24h_usd"]]


# 3) Append to an existing workbook as a NEW sheet (or create if missing)
from pathlib import Path
out_path   = "crypto_market_data.xlsx"          # your master workbook
sheet_name = "btc_7d_usd"                       # name the sheet for clarity


if Path(out_path).exists():
    # Append; if the sheet already exists, REPLACE it (safer for reruns)
    with pd.ExcelWriter(out_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as xw:
        df.to_excel(xw, index=False, sheet_name=sheet_name)
else:
    # Create the workbook and write the first sheet
    with pd.ExcelWriter(out_path, engine="openpyxl") as xw:
        df.to_excel(xw, index=False, sheet_name=sheet_name)


print(f"Saved sheet '{sheet_name}' in {out_path}")
