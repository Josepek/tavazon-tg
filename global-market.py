# global_market.py
import yfinance as yf
from utils import format_value_number_custom, send_message

SYMBOLS = {
    "BTCUSDT": "BTC-USD",
    "ETHUSDT": "ETH-USD",
    "UKOIL": "BZ=F",      
    "COPPER": "HG=F",   
    "ZINC": "ZNC=F",     
    "GOLD": "GC=F",     
    "ALUMINIUM": "ALI=F",     
    "SP500": "^GSPC",      
    "DJI": "^DJI",      
    "NASDAQ": "^IXIC",    
    "DXY": "DX-Y.NYB",    
    "EURUSD": "EURUSD=X", 
}

DISPLAY_NAMES = {
    "BTCUSDT": "بیت‌کوین",
    "ETHUSDT": "اتریوم",
    "UKOIL": "نفت برنت",
    "COPPER": "مس",
    "ZINC": "روی",
    "GOLD": "طلا",
    "ALUMINIUM": "آلومینیوم",
    "SP500": "اس‌اند‌پی ۵۰۰",
    "DJI": "داوجونز",
    "NASDAQ": "نزدک",
    "DXY": "شاخص دلار",
    "EURUSD": "یورو / دلار",
}

FOOTER = "\n\nکارگزاری توازن بازار\nثبت‌نام ۳ کلیک در بورس:\nregister.dayatrader.ir\n\n🆔 @Tavazonex\n🔊 tavazonex.com"


def fetch_market_data():
    results = {}
    for key, symbol in SYMBOLS.items():
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="2d")
            if not data.empty:
                latest = data["Close"].iloc[-1]
                prev = data["Close"].iloc[-2] if len(data) > 1 else latest
                change = latest - prev
                change_percent = (change / prev) * 100 if prev else 0
                results[key] = {
                    "price": latest,
                    "change": change_percent,
                }
            else:
                results[key] = None
        except Exception as e:
            print(f"⚠️ Error in fetch data {key}: {e}")
            results[key] = None
    return results


def build_market_message(data):
    msg = ["🌍 <b>گزارش بازار جهانی امروز</b>\n"]

    for key, info in data.items():
        if not info:
            continue

        name = DISPLAY_NAMES.get(key, key)
        price = format_value_number_custom(info["price"], 2)
        change = info["change"]

        # علامت + یا -
        if change > 0:
            change_text = f"({format_value_number_custom(round(abs(change), 2))}٪+)"
        elif change < 0:
            change_text = f"({format_value_number_custom(round(abs(change), 2))}٪-)"
        else:
            change_text = "(۰٪)"

        msg.append(f"- <b>{name}:</b> {price} {change_text}")

    msg.append(FOOTER)
    return "\n".join(msg)


if __name__ == "__main__":
    data = fetch_market_data()
    message = build_market_message(data)
    send_message(message)
