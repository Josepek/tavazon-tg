import requests

BOT_TOKEN = "7943524257:AAFnRP8cn20kvyeC5FtobmL71mmbvvel0p4"
CHANNEL_USERNAME = "@pepektest"

def send_message(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_USERNAME,
            "text": message,
            "parse_mode": "HTML"
        }
        resp = requests.post(url, json=payload)
        if resp.status_code == 200:
            print("📨 Send message successfully")
        else:
            print(f"⚠️ send message failed!: {resp.text}")
    except Exception as e:
        print(f"❌ error in sending message: {e}")

def format_value_number_custom(value, digits=0):
    try:
        value = round(float(value), digits)
        formatted = f"{value:,.{digits}f}"
        return formatted.translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))
    except:
        return str(value)

def format_change(value):
    try:
        value = float(value)
        if value > 0:
            return f"🔺 {format_value_number_custom(value)}"
        elif value < 0:
            return f"🔻 {format_value_number_custom(abs(value))}"
        else:
            return "➖ ۰"
    except:
        return str(value)

def read_data(file_path):
    import json
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}
