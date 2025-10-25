import requests
from utils import format_value_number_custom, format_change, send_message

TSE_URL = "https://cdn.tsetmc.com/api/MarketData/GetMarketOverview/1"
IFB_URL = "https://cdn.tsetmc.com/api/MarketData/GetMarketOverview/2"

FOOTER = (
    "\n\nثبت‌نام ۳ کلیک در بورس:\nhttps://B2n.ir/tvzn\n\n🆔 @Tavazonex"
)

def fetch_market_data(url):
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json().get("marketOverview") or resp.json().get("data")
        return data
    except Exception as e:
        print(f"❌ Error fetching market data: {e}")
        return None

def build_tse_message(data):
    msg = [
        "وضعیت بازار",
        "",
        "بورس:",
        f"🔹 شاخص کل: {format_value_number_custom(data.get('indexLastValue', 0), 2)} ({format_change(data.get('indexChange', 0))})",
        f"🔹 شاخص هم‌وزن: {format_value_number_custom(data.get('indexEqualWeightedLastValue', 0), 2)} ({format_change(data.get('indexEqualWeightedChange', 0))})",
        f"▪️ ارزش معاملات: {format_value_number_custom(data.get('marketActivityQTotCap', 0) / 10_000_000, 3)} B",
        f"▪️ حجم معاملات: {format_value_number_custom(data.get('marketActivityQTotTran', 0) / 1_000_000_000, 3)} B",
        f"▪️ تعداد معاملات: {format_value_number_custom(data.get('marketActivityZTotTran', 0), 0)}",
        "",
    ]
    return "\n".join(msg)

def build_ifb_message(data):
    msg = [
        "فرابورس:",
        f"🔹 شاخص کل: {format_value_number_custom(data.get('indexLastValue', 0), 2)} ({format_change(data.get('indexChange', 0))})",
        f"▪️ ارزش بازار پایه: {format_value_number_custom(data.get('marketValueBase', 0) / 1_000_000_000, 2)} B",
        f"▪️ ارزش بازار اول و دوم: {format_value_number_custom(data.get('marketValue', 0) / 1_000_000_000, 2)} B",
        f"▪️ ارزش معاملات: {format_value_number_custom(data.get('marketActivityQTotCap', 0) / 1_000_000_000, 3)} B",
        f"▪️ تعداد معاملات: {format_value_number_custom(data.get('marketActivityZTotTran', 0), 0)}",
    ]
    return "\n".join(msg)

if __name__ == "__main__":
    tse_data = fetch_market_data(TSE_URL)
    ifb_data = fetch_market_data(IFB_URL)

    if tse_data and ifb_data:
        message = build_tse_message(tse_data) + "\n" + build_ifb_message(ifb_data) + FOOTER
        send_message(message)
    else:
        print("⚠️ Could not fetch market data.")