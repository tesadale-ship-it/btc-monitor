import requests
import csv
import os
from datetime import datetime

CSV_FILE = "crypto_history.csv"

def get_coingecko_prices():
    """BTC + ETH 가격 (CoinGecko)"""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,ethereum",
        "vs_currencies": "usd,krw",
        "include_24hr_change": "true"
    }
    res = requests.get(url, params=params).json()
    return {
        "btc_usd": res["bitcoin"]["usd"],
        "btc_krw": res["bitcoin"]["krw"],
        "btc_24h_change": round(res["bitcoin"]["usd_24h_change"], 2),
        "eth_usd": res["ethereum"]["usd"],
        "eth_krw": res["ethereum"]["krw"],
        "eth_24h_change": round(res["ethereum"]["usd_24h_change"], 2),
    }

def get_blockchair_stats(chain):
    """Blockchair에서 네트워크 통계 (BTC 또는 ETH)"""
    url = f"https://api.blockchair.com/{chain}/stats"
    res = requests.get(url).json()
    data = res.get("data", {})
    return {
        "blocks": data.get("blocks"),
        "transactions_24h": data.get("transactions_24h"),
        "mempool_transactions": data.get("mempool_transactions"),
        "avg_tx_fee_usd": round(data.get("average_transaction_fee_usd_24h", 0), 4),
        "mempool_size": data.get("mempool_size"),
    }

def get_fear_greed():
    """공포탐욕지수"""
    url = "https://api.alternative.me/fng/"
    res = requests.get(url).json()
    return int(res["data"][0]["value"]), res["data"][0]["value_classification"]

def save_to_csv(row):
    file_exists = os.path.exists(CSV_FILE)
    headers = [
        "날짜 (UTC)",
        # BTC 가격 정보
        "BTC (USD)", "BTC (KRW)", "BTC 24h 변동률(%)",
        # BTC 네트워크 정보
        "BTC 블록 수", "BTC 24h 거래수", "BTC 평균 수수료 (USD)", "BTC Mempool 거래수",
        # ETH 가격 정보
        "ETH (USD)", "ETH (KRW)", "ETH 24h 변동률(%)",
        # ETH 네트워크 정보
        "ETH 블록 수", "ETH 24h 거래수", "ETH 평균 수수료 (USD)", "ETH Mempool 거래수",
        # 심리 지표
        "공포탐욕지수", "시장상태",
    ]
    with open(CSV_FILE, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow(row)
    print(f"✅ CSV 저장 완료: {CSV_FILE}")

def main():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    print("📡 데이터 수집 중...")
    
    prices = get_coingecko_prices()
    btc_net = get_blockchair_stats("bitcoin")
    eth_net = get_blockchair_stats("ethereum")
    fng_value, fng_label = get_fear_greed()
    
    print(f"\n📅 날짜: {now}")
    print(f"💰 BTC: ${prices['btc_usd']:,} ({prices['btc_24h_change']:+.2f}%)")
    print(f"   └ 24h 거래수: {btc_net['transactions_24h']:,} / 평균 수수료: ${btc_net['avg_tx_fee_usd']}")
    print(f"💰 ETH: ${prices['eth_usd']:,} ({prices['eth_24h_change']:+.2f}%)")
    print(f"   └ 24h 거래수: {eth_net['transactions_24h']:,} / 평균 수수료: ${eth_net['avg_tx_fee_usd']}")
    print(f"😨 공포탐욕지수: {fng_value} ({fng_label})")
    
    row = [
        now,
        prices["btc_usd"], prices["btc_krw"], prices["btc_24h_change"],
        btc_net["blocks"], btc_net["transactions_24h"], btc_net["avg_tx_fee_usd"], btc_net["mempool_transactions"],
        prices["eth_usd"], prices["eth_krw"], prices["eth_24h_change"],
        eth_net["blocks"], eth_net["transactions_24h"], eth_net["avg_tx_fee_usd"], eth_net["mempool_transactions"],
        fng_value, fng_label,
    ]
    save_to_csv(row)

if __name__ == "__main__":
    main()
    