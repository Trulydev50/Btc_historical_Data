# Btc_historical_Data
How to Download Bitcoin Historical Price Data 
Install dependencies from requirements.txt:

pip install -r requirements.txt


🔑 API Keys

Go to CoinGecko API docs
.

Create a file named keys.json in your project folder:

{
  "x-cg-demo-api-key": "YOUR_DEMO_KEY",
  "x-cg-pro-api-key":  "YOUR_PRO_KEY"
}


Update the file path in the script if needed.

⚠️ Do not commit your real keys.json — only keep it locally. A sample file (keys.json.sample) is included here.

▶️ How to Run

Run the script:

python btc_history_example.py


Expected output (Demo mode):

Loaded demo key (last 4): XXXX
PING: {'gecko_says': '(V3) To the Moon!'}
First 2 prices: [[TIMESTAMP, PRICE], [TIMESTAMP, PRICE]]
Saved sheet 'btc_7d_usd' in crypto_market_data.xlsx


This creates crypto_market_data.xlsx with a clean sheet of historical data.

⚙️ Customization

Change these parameters to suit your needs:

params →

vs_currency: "usd", "eur", "sgd", etc.

days: "1", "7", "30", "90", "max"

interval: "daily", "hourly"

sheet_name: rename the Excel sheet (e.g., btc_30d_eur).

out_path: set the filename/path of the Excel workbook.

🚀 Switching to Pro

To use the Pro API, update these lines:

key = get_pro_key()
headers = {"accept": "application/json", "x-cg-pro-api-key": key}
base_url = PUB_PRO_URL


Everything else remains the same.

📚 Related Guides

Download Crypto OHLCV Data

How to Pull Crypto Prices from DEXs

Import Crypto Prices into Google Sheets

Crypto Exit Strategy Spreadsheet Template

AI-Powered Crypto Research with MCP

Get Token Holders
