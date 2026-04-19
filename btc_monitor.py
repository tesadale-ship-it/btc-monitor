import requests
import csv
import os
from datetime import datetime

CSV_FILE = "btc_history.csv"

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin", "vs_currencies": "usd,krw"}
    res = requests.get(url, params=params).json()
    return res["bitcoin"]["usd"], res["bitcoin"]["krw"]

def get_fear_greed():
    url = "https://api.alternative.me/fng/"
    res = requests.get(url).json()
    value = res["data"][0]["value"]
    label = res["data"][0]["value_classification"]
    return int(value), label

def save_to_csv(date, btc_usd, btc_krw, fng_value, fng_label):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["날짜", "BTC (USD)", "BTC (KRW)", "공포탐욕지수", "시장상태"])
        writer.writerow([date, btc_usd, btc_krw, fng_value, fng_label])
    print(f"✅ CSV 저장 완료: {CSV_FILE}")

def main():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    print("📡 데이터 가져오는 중...")
    btc_usd, btc_krw = get_btc_price()
    fng_value, fng_label = get_fear_greed()
    print(f"📅 날짜: {now}")
    print(f"💰 BTC: ${btc_usd:,} USD / ₩{btc_krw:,} KRW")
    print(f"😨 공포탐욕지수: {fng_value} ({fng_label})")
    save_to_csv(now, btc_usd, btc_krw, fng_value, fng_label)

if __name__ == "__main__":
    main()
