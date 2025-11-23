from datetime import date, timedelta
import random


class MockBrokerConnector:
    def __init__(self, broker_name: str = "MockBroker"):
        self.broker_name = broker_name

    def fetch_accounts(self):
        return [{"account_id": "ACC123", "currency": "USD"}]

    def fetch_positions(self):
        symbols = ["AAPL", "TSLA", "0700.HK", "600519.SS"]
        positions = []
        for sym in symbols:
            quantity = random.randint(10, 100)
            price = random.uniform(50, 300)
            positions.append({
                "symbol": sym,
                "market": "US" if "." not in sym else ("HK" if "HK" in sym else "CN"),
                "name": f"{sym} Corp",
                "quantity": quantity,
                "avg_cost": round(price * 0.9, 2),
                "last_price": round(price, 2)
            })
        return positions

    def fetch_transactions(self, start_date: date, end_date: date):
        txs = []
        cur = start_date
        while cur <= end_date:
            txs.append({
                "trade_date": cur,
                "symbol": "AAPL",
                "market": "US",
                "side": random.choice(["buy", "sell"]),
                "quantity": random.randint(1, 5),
                "price": random.uniform(100, 200),
                "fees": random.uniform(0, 2)
            })
            cur += timedelta(days=7)
        return txs
