from datetime import date, datetime, timedelta
import random
from typing import List


class MockDataSource:
    markets = ["CN", "HK", "US"]

    def fetch_price_history(self, symbol: str, market: str, start_date: date, end_date: date):
        data = []
        cur = start_date
        price = random.uniform(10, 200)
        while cur <= end_date:
            change = random.uniform(-2, 2)
            open_price = price
            close_price = max(1, price + change)
            high = max(open_price, close_price) + random.random()
            low = min(open_price, close_price) - random.random()
            volume = random.uniform(1e5, 5e6)
            data.append({
                "date": cur,
                "open": round(open_price, 2),
                "high": round(high, 2),
                "low": round(low, 2),
                "close": round(close_price, 2),
                "adj_close": round(close_price, 2),
                "volume": round(volume, 2)
            })
            price = close_price
            cur += timedelta(days=1)
        return data

    def fetch_quote(self, symbol: str, market: str):
        return {
            "symbol": symbol,
            "market": market,
            "price": round(random.uniform(10, 200), 2),
            "change_pct": round(random.uniform(-5, 5), 2)
        }

    def fetch_fundamentals(self, symbol: str, market: str):
        return [{
            "period_end_date": date.today() - timedelta(days=90 * i),
            "revenue": random.uniform(1e8, 1e10),
            "net_income": random.uniform(1e7, 1e9),
            "eps": random.uniform(0.1, 10),
            "roe": random.uniform(0, 30),
            "gross_margin": random.uniform(10, 60),
            "operating_margin": random.uniform(5, 40),
            "pe_ttm": random.uniform(5, 40),
            "pb": random.uniform(0.5, 10),
            "dividend_yield": random.uniform(0, 5),
        } for i in range(3)]

    def fetch_news(self, symbol: str, market: str, limit: int = 5):
        now = datetime.utcnow()
        return [{
            "title": f"{symbol} news headline {i}",
            "source": "MockWire",
            "url": "https://example.com/news",
            "published_at": now - timedelta(hours=i * 5),
            "summary": "Mock summary"
        } for i in range(limit)]

    def fetch_research_notes(self, symbol: str, market: str, limit: int = 3):
        now = datetime.utcnow()
        return [{
            "broker_name": "MockBroker",
            "title": f"Research on {symbol} #{i}",
            "url": "https://example.com/research",
            "published_at": now - timedelta(days=i),
            "rating": random.choice(["Buy", "Hold", "Sell"]),
            "target_price": random.uniform(10, 300),
            "summary": "Mock research summary"
        } for i in range(limit)]
