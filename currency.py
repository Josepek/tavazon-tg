import requests
from utils import format_value_number_custom, send_message

CURRENCY_URL = "https://chandshode.com/api/Gold_Currency.php?fields=currency"

TARGET_SYMBOLS = ["USDT_IRT", "USD", "EUR", "AED", "GBP"]

FOOTER = (
    "\n\nثبت‌نام ۳ کلیک در بورس:\nhttps://B2n.ir/tvzn\n\n🆔 @Tavazonex"
)

def fetch_currency_data():
    try:
        resp = requests.get(CURRENCY_URL, timeout=15)
        resp.raise_for_status()
        result = resp.json()
        data = result.get("data", {}).get("currency", [])
        filtered = [item for item in data if item.get("symbol") in TARGET_SYMBOLS]
        return filtered
    except Exception as e:
        print(f"❌ Error fetching currency data: {e}")
        return []

def build_currency_message(data):
    msg = ["💵 نرخ ارزها:"]
    for item in data:
        name = item.get("name", "")
        price = item.get("price", 0)
        msg.append(f"🔹 {name}: {format_value_number_custom(price)} تومان")
    return "\n".join(msg)

if __name__ == "__main__":
    currency_data = fetch_currency_data()
    if currency_data:
        message = build_currency_message(currency_data) + FOOTER
        send_message(message)