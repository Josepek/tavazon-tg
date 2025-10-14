import requests
from utils import format_value_number_custom, send_message

GOLD_URL = "https://chandshode.com/api/Gold_Currency.php?fields=gold"

SELECTED_SYMBOLS = [
    "IR_GOLD_18K",
    "IR_GOLD_24K",
    "IR_COIN_QUARTER",
    "Half Coin",
    "IR_COIN_EMAMI",
    "IR_COIN_BAHAR"
]

def fetch_gold_data():
    try:
        resp = requests.get(GOLD_URL, timeout=15)
        resp.raise_for_status()
        result = resp.json()
        gold_items = result.get("data", {}).get("gold", [])
        filtered = [g for g in gold_items if g.get("symbol") in SELECTED_SYMBOLS]
        return filtered
    except Exception as e:
        print(f"❌ خطا در دریافت داده‌های طلا: {e}")
        return []

def build_gold_message(gold_data):
    msg = ["💰 گزارش قیمت طلا و سکه:"]
    for item in gold_data:
        name = item.get("name", item.get("title", ""))
        price = format_value_number_custom(item.get("price", 0))
        msg.append(f"🔸 {name}: {price} تومان")
    return "\n".join(msg)

if __name__ == "__main__":
    gold_data = fetch_gold_data()
    if gold_data:
        message = build_gold_message(gold_data)
        footer = "\n\nکارگزاری توازن بازار\nثبت‌نام ۳ کلیک در بورس:\nregister.dayatrader.ir\n\n🆔 @Tavazonex\n🔊 tavazonex.com"
        send_message(message + footer)
