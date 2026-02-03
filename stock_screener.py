#!/usr/bin/env python3
"""
Low-Float Stock Screener for Day Trading
========================================
A scanner designed for Kos to find low-float day trading opportunities
with high relative volume and news catalysts.

Features:
- Screens stocks under $20 with float under 50M
- Identifies volume spikes (2x+ average)
- Checks for news catalysts
- Generates actionable alerts with entry/exit zones

Author: OpenClaw Agent
Target User: Kos (Day Trader)
"""

import requests
import json
import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional
from statistics import mean
import time

# =============================================================================
# CONFIGURATION - Adjust these settings as needed
# =============================================================================

CONFIG = {
    # Price & Float Filters
    "max_price": 20.0,           # Maximum stock price ($)
    "min_price": 0.50,           # Minimum stock price (filter out sub-penny)
    "max_float": 50_000_000,     # Maximum float (shares)
    
    # Volume Criteria
    "relative_volume_threshold": 2.0,  # Current vol must be 2x average
    "min_avg_volume": 50_000,    # Minimum average daily volume
    
    # Data Sources
    "api_key": "YOUR_API_KEY",   # Replace with Finnhub/Polygon key
    "provider": "yahoo_fallback",  # Options: finnhub, polygon, yahoo_fallback
    
    # Scan Settings
    "scan_limit": 500,           # Max stocks to analyze per run
    "request_delay": 0.1,        # Seconds between API calls (rate limiting)
    
    # Alert Settings
    "risk_per_trade": 0.02,      # 2% account risk per trade (for position sizing)
    "stop_loss_pct": 0.05,       # 5% stop loss suggestion
    
    # Output
    "output_format": "console",   # Options: console, json, csv
    "min_alert_score": 3,        # Minimum total score to trigger alert (1-5 scale)
}

# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class StockAlert:
    """Represents a single trading opportunity alert."""
    ticker: str
    price: float
    float_shares: int
    relative_volume: float
    avg_volume: int
    current_volume: int
    news_catalyst: bool
    news_headlines: List[str]
    entry_zone: tuple  # (low, high)
    stop_loss: float
    target_1: float    # First profit target (1:1 R/R)
    target_2: float    # Second profit target (2:1 R/R)
    score: int         # 1-5 score based on setup quality
    catalyst_tags: List[str]
    timestamp: str
    
    def to_dict(self) -> Dict:
        """Convert alert to dictionary for JSON export."""
        return {
            "ticker": self.ticker,
            "price": self.price,
            "float": self.float_shares,
            "relative_volume": self.relative_volume,
            "avg_volume": self.avg_volume,
            "current_volume": self.current_volume,
            "has_news": self.news_catalyst,
            "news": self.news_headlines[:3],  # Top 3 headlines
            "entry_zone": f"${self.entry_zone[0]:.2f} - ${self.entry_zone[1]:.2f}",
            "stop_loss": f"${self.stop_loss:.2f}",
            "target_1": f"${self.target_1:.2f}",
            "target_2": f"${self.target_2:.2f}",
            "score": self.score,
            "catalysts": self.catalyst_tags,
            "timestamp": self.timestamp
        }


# =============================================================================
# LOGGING SETUP
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stock_screener.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# =============================================================================
# DATA FETCHING MODULE
# =============================================================================

class DataProvider:
    """Abstracts data fetching from various sources."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.api_key = config.get("api_key")
        self.provider = config.get("provider", "yahoo_fallback")
        self.delay = config.get("request_delay", 0.1)
        self.session = requests.Session()
        
    def _rate_limit(self):
        """Respect rate limits between requests."""
        time.sleep(self.delay)
        
    def get_stock_universe(self) -> List[str]:
        """
        Get list of stock tickers to scan.
        Returns a diversified list of potential low-float candidates.
        """
        # Start with known active low-float candidates
        # In production, you'd fetch from an exchange listing API
        active_tickers = [
            # Small cap movers - dynamically updated list
            "MULN", "TTOO", "NVOS", "GME", "AMC", "BBBY", "APE", 
            "SPRC", "LGMK", "ATNF", "DBGI", "CRKN", "APDN",
            # Add more as needed
        ]
        return active_tickers[:self.config["scan_limit"]]
    
    def get_quote(self, ticker: str) -> Optional[Dict]:
        """Fetch current stock quote with price and volume."""
        self._rate_limit()
        
        try:
            if self.provider == "finnhub" and self.api_key != "YOUR_API_KEY":
                return self._fetch_finnhub_quote(ticker)
            elif self.provider == "polygon" and self.api_key != "YOUR_API_KEY":
                return self._fetch_polygon_quote(ticker)
            else:
                return self._fetch_yahoo_quote(ticker)
        except Exception as e:
            logger.warning(f"Error fetching quote for {ticker}: {e}")
            return None
    
    def _fetch_yahoo_quote(self, ticker: str) -> Optional[Dict]:
        """Fetch from Yahoo Finance (free, no API key needed for basic data)."""
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        params = {
            "interval": "1d",
            "range": "1mo"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; StockScreener/1.0)"
        }
        
        response = self.session.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None
            
        data = response.json()
        
        if not data.get("chart", {}).get("result"):
            return None
            
        result = data["chart"]["result"][0]
        meta = result["meta"]
        
        # Get price from meta or latest close
        current_price = meta.get("regularMarketPrice", meta.get("previousClose", 0))
        
        # Get volume data
        volumes = result.get("indicators", {}).get("quote", [{}])[0].get("volume", [])
        valid_volumes = [v for v in volumes if v is not None]
        
        if len(valid_volumes) >= 2:
            current_volume = valid_volumes[-1]
            avg_volume = mean(valid_volumes[:-1])  # Exclude today
        else:
            current_volume = 0
            avg_volume = 0
            
        return {
            "ticker": ticker,
            "price": float(current_price),
            "current_volume": int(current_volume) if current_volume else 0,
            "avg_volume": int(avg_volume),
            "currency": meta.get("currency", "USD"),
            "exchange": meta.get("exchangeName", ""),
            "timestamp": datetime.now().isoformat()
        }
    
    def _fetch_finnhub_quote(self, ticker: str) -> Optional[Dict]:
        """Fetch from Finnhub (requires API key)."""
        url = f"https://finnhub.io/api/v1/quote"
        params = {
            "symbol": ticker,
            "token": self.api_key
        }
        
        response = self.session.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "ticker": ticker,
                "price": data.get("c", 0),
                "current_volume": 0,  # Finnhub quote doesn't include volume
                "avg_volume": 0,
                "timestamp": datetime.now().isoformat()
            }
        return None
    
    def _fetch_polygon_quote(self, ticker: str) -> Optional[Dict]:
        """Fetch from Polygon.io (requires API key)."""
        today = datetime.now().strftime("%Y-%m-%d")
        url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{today}/{today}"
        params = {"apiKey": self.api_key}
        
        response = self.session.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            if results:
                return {
                    "ticker": ticker,
                    "price": results[0].get("c", 0),
                    "current_volume": results[0].get("v", 0),
                    "avg_volume": 0,
                    "timestamp": datetime.now().isoformat()
                }
        return None
    
    def get_float_data(self, ticker: str) -> Optional[int]:
        """Get stock float (shares available for trading)."""
        # Note: Float data often requires paid APIs or web scraping
        # This is a simplified implementation
        
        self._rate_limit()
        
        # Try Yahoo Finance first
        url = f"https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}"
        params = {"modules": "defaultKeyStatistics"}
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                stats = data.get("quoteSummary", {}).get("result", [{}])[0].get("defaultKeyStatistics", {})
                float_data = stats.get("floatShares", {})
                if float_data:
                    return int(float_data.get("raw", 0))
        except Exception as e:
            logger.debug(f"Could not fetch float for {ticker}: {e}")
            
        return None
    
    def get_news(self, ticker: str) -> List[Dict]:
        """Fetch recent news for a ticker."""
        self._rate_limit()
        
        try:
            # Use Yahoo Finance news API (free)
            url = f"https://query1.finance.yahoo.com/v1/finance/search"
            params = {
                "q": ticker,
                "quotesCount": 0,
                "newsCount": 5
            }
            headers = {"User-Agent": "Mozilla/5.0"}
            
            response = self.session.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                news = data.get("news", [])
                
                # Filter news from last 48 hours
                cutoff = datetime.now() - timedelta(hours=48)
                recent_news = []
                
                for item in news:
                    pub_date = datetime.fromtimestamp(item.get("providerPublishTime", 0))
                    if pub_date > cutoff:
                        recent_news.append({
                            "headline": item.get("title", ""),
                            "publisher": item.get("publisher", ""),
                            "url": item.get("link", ""),
                            "time": pub_date.isoformat()
                        })
                        
                return recent_news
        except Exception as e:
            logger.debug(f"Could not fetch news for {ticker}: {e}")
            
        return []


# =============================================================================
# ANALYSIS MODULE
# =============================================================================

class StockAnalyzer:
    """Analyzes stocks for day trading opportunities."""
    
    # Catalyst keywords to scan for in news
    CATALYST_KEYWORDS = [
        "earnings", "revenue", "profit", "loss", "guidance",
        "FDA", "approval", "trial", "clinical", "drug", "pipeline",
        "merger", "acquisition", "buyout", "takeover", "deal",
        "partnership", "contract", "order", "expansion",
        "patent", "lawsuit", "settlement",
        "upgrade", "downgrade", "target", "initiate",
        "shareholder", "investor", "board", "CEO", "executive",
        "offering", "dilution", "warrant", "exercise"
    ]
    
    def __init__(self, config: Dict):
        self.config = config
        
    def calculate_relative_volume(self, current: int, average: int) -> float:
        """Calculate relative volume ratio."""
        if average == 0:
            return 0
        return round(current / average, 2)
    
    def analyze_news(self, news_items: List[Dict]) -> tuple:
        """
        Analyze news for catalysts.
        Returns: (has_catalyst, catalyst_tags, top_headlines)
        """
        has_catalyst = False
        catalyst_tags = []
        headlines = []
        
        for item in news_items:
            headline = item.get("headline", "").lower()
            headlines.append(item.get("headline", ""))
            
            for keyword in self.CATALYST_KEYWORDS:
                if keyword in headline and keyword not in catalyst_tags:
                    catalyst_tags.append(keyword)
                    has_catalyst = True
                    
        return has_catalyst, catalyst_tags, headlines
    
    def calculate_entry_exit(self, price: float, avg_volume: int, 
                            current_volume: int, has_catalyst: bool) -> Dict:
        """
        Calculate suggested entry/exit zones based on price action.
        
        For low-float stocks:
        - Entry: Near current price with confirmation
        - Stop: Based on volatility (typically -5% to -8%)
        - Targets: 1:1 and 2:1 risk/reward ratios
        """
        # Volatility adjustment based on float/volume
        vol_factor = min(current_volume / max(avg_volume, 1), 5)  # Cap at 5x
        
        # Wider stops for higher volatility
        if vol_factor > 3:
            stop_pct = 0.08  # 8% for very volatile
        elif vol_factor > 2:
            stop_pct = 0.06  # 6% for volatile  
        else:
            stop_pct = 0.05  # 5% base
            
        # Reduce stop if catalyst present (momentum play)
        if has_catalyst:
            stop_pct = min(stop_pct, 0.05)
            
        stop_loss = price * (1 - stop_pct)
        risk = price - stop_loss
        
        # Targets based on risk/reward
        target_1 = price + risk  # 1:1
        target_2 = price + (risk * 2)  # 2:1
        
        # Entry zone: slight pullback or current breakout
        entry_low = max(price * 0.98, stop_loss * 1.01)  # Don't chase too high
        entry_high = price * 1.02
        
        return {
            "entry_zone": (round(entry_low, 2), round(entry_high, 2)),
            "stop_loss": round(stop_loss, 2),
            "target_1": round(target_1, 2),
            "target_2": round(target_2, 2),
            "risk_pct": round(stop_pct * 100, 1)
        }
    
    def calculate_score(self, relative_vol: float, has_catalyst: bool, 
                       catalyst_tags: List[str], price: float) -> int:
        """
        Calculate setup quality score (1-5).
        
        Scoring:
        - Base: 1 point
        - High relative volume (>2x): +1
        - Very high relative volume (>4x): +1
        - Has news catalyst: +1
        - Multiple catalysts (>2 tags): +1
        - Good price range ($2-$10 sweet spot): +1 bonus
        """
        score = 1  # Base score
        
        if relative_vol >= 2:
            score += 1
        if relative_vol >= 4:
            score += 1
        if has_catalyst:
            score += 1
        if len(catalyst_tags) > 2:
            score += 1
        # Price sweet spot for day trading
        if 2 <= price <= 10:
            score = min(score + 1, 5)
            
        return min(score, 5)


# =============================================================================
# SCANNER ENGINE
# =============================================================================

class StockScreener:
    """Main screener engine that orchestrates the scanning process."""
    
    def __init__(self, config: Dict = None):
        self.config = config or CONFIG
        self.provider = DataProvider(self.config)
        self.analyzer = StockAnalyzer(self.config)
        self.alerts: List[StockAlert] = []
        
    def scan(self) -> List[StockAlert]:
        """
        Run the full scan and return actionable alerts.
        """
        logger.info("=" * 60)
        logger.info("Starting Low-Float Stock Scan")
        logger.info(f"Filters: Price < ${self.config['max_price']}, Float < {self.config['max_float']:,}")
        logger.info(f"Volume Threshold: {self.config['relative_volume_threshold']}x average")
        logger.info("=" * 60)
        
        tickers = self.provider.get_stock_universe()
        logger.info(f"Scanning {len(tickers)} tickers...")
        
        alerts = []
        
        for i, ticker in enumerate(tickers, 1):
            logger.info(f"[{i}/{len(tickers)}] Analyzing {ticker}...")
            
            try:
                alert = self._analyze_ticker(ticker)
                if alert and alert.score >= self.config["min_alert_score"]:
                    alerts.append(alert)
                    logger.info(f"  ✓ ALERT: {ticker} - Score: {alert.score}/5")
            except Exception as e:
                logger.error(f"  ✗ Error analyzing {ticker}: {e}")
                continue
                
        # Sort by score (highest first), then by relative volume
        alerts.sort(key=lambda x: (x.score, x.relative_volume), reverse=True)
        
        self.alerts = alerts
        logger.info(f"\nScan complete. Found {len(alerts)} actionable alerts.")
        
        return alerts
    
    def _analyze_ticker(self, ticker: str) -> Optional[StockAlert]:
        """Analyze a single ticker and return alert if criteria met."""
        
        # 1. Get quote data
        quote = self.provider.get_quote(ticker)
        if not quote:
            return None
            
        price = quote.get("price", 0)
        current_volume = quote.get("current_volume", 0)
        avg_volume = quote.get("avg_volume", 0)
        
        # 2. Apply price filter
        if not (self.config["min_price"] <= price <= self.config["max_price"]):
            return None
            
        # 3. Apply volume filter
        if avg_volume < self.config["min_avg_volume"]:
            return None
            
        relative_volume = self.analyzer.calculate_relative_volume(current_volume, avg_volume)
        if relative_volume < self.config["relative_volume_threshold"]:
            return None
            
        # 4. Get float data (if available)
        float_shares = self.provider.get_float_data(ticker)
        if float_shares and float_shares > self.config["max_float"]:
            return None
        if not float_shares:
            float_shares = 0  # Unknown, will flag in output
            
        # 5. Check for news catalysts
        news = self.provider.get_news(ticker)
        has_catalyst, catalyst_tags, headlines = self.analyzer.analyze_news(news)
        
        # 6. Calculate entry/exit zones
        levels = self.analyzer.calculate_entry_exit(
            price, avg_volume, current_volume, has_catalyst
        )
        
        # 7. Calculate quality score
        score = self.analyzer.calculate_score(
            relative_volume, has_catalyst, catalyst_tags, price
        )
        
        # 8. Create alert
        return StockAlert(
            ticker=ticker,
            price=price,
            float_shares=float_shares,
            relative_volume=relative_volume,
            avg_volume=avg_volume,
            current_volume=current_volume,
            news_catalyst=has_catalyst,
            news_headlines=headlines,
            entry_zone=levels["entry_zone"],
            stop_loss=levels["stop_loss"],
            target_1=levels["target_1"],
            target_2=levels["target_2"],
            score=score,
            catalyst_tags=catalyst_tags,
            timestamp=datetime.now().isoformat()
        )


# =============================================================================
# OUTPUT MODULE
# =============================================================================

class AlertOutput:
    """Formats and outputs alerts in various formats."""
    
    @staticmethod
    def console(alerts: List[StockAlert]):
        """Print alerts to console with nice formatting."""
        if not alerts:
            print("\n" + "=" * 60)
            print("NO ALERTS FOUND")
            print("No stocks met the scan criteria at this time.")
            print("=" * 60)
            return
            
        print("\n" + "=" * 60)
        print("🚨 LOW-FLOAT DAY TRADING ALERTS 🚨")
        print("=" * 60)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Alerts: {len(alerts)}")
        print("=" * 60)
        
        for alert in alerts:
            AlertOutput._print_single_alert(alert)
            
        print("\n" + "=" * 60)
        print("⚠️  DISCLAIMER: These are algorithmic alerts for review only.")
        print("   Always conduct your own analysis before trading.")
        print("=" * 60)
    
    @staticmethod
    def _print_single_alert(alert: StockAlert):
        """Print a single alert in formatted console output."""
        float_str = f"{alert.float_shares:,}" if alert.float_shares else "Unknown"
        
        stars = "★" * alert.score + "☆" * (5 - alert.score)
        
        print(f"\n┌{'─' * 58}┐")
        print(f"│ {alert.ticker:9} | ${alert.price:>7.2f} | Float: {float_str:>12} │")
        print(f"│ {'SCORE: ' + stars:56} │")
        print(f"├{'─' * 58}┤")
        print(f"│ VOLUME: {alert.relative_volume:.1f}x avg ({alert.avg_volume:,} → {alert.current_volume:,}){' ' * 10}│")
        
        if alert.news_catalyst:
            print(f"│ 🔔 CATALYST: {', '.join(alert.catalyst_tags[:3]):43} │")
            for headline in alert.news_headlines[:2]:
                short = headline[:52] + "..." if len(headline) > 55 else headline
                print(f"│   • {short:53} │")
        else:
            print(f"│ 🚫 No recent news catalysts detected{' ' * 18} │")
            
        print(f"├{'─' * 58}┤")
        print(f"│ ENTRY ZONE: ${alert.entry_zone[0]:.2f} - ${alert.entry_zone[1]:.2f}{' ' * 28} │")
        print(f"│ STOP LOSS:  ${alert.stop_loss:.2f} ({alert.price - alert.stop_loss:.2f} risk){' ' * 25} │")
        print(f"│ TARGET 1:   ${alert.target_1:.2f} (1:1 R/R){' ' * 28} │")
        print(f"│ TARGET 2:   ${alert.target_2:.2f} (2:1 R/R){' ' * 28} │")
        print(f"└{'─' * 58}┘")
    
    @staticmethod
    def json_export(alerts: List[StockAlert], filename: str = None):
        """Export alerts to JSON file or string."""
        data = {
            "generated_at": datetime.now().isoformat(),
            "total_alerts": len(alerts),
            "config": {
                "max_price": CONFIG["max_price"],
                "max_float": CONFIG["max_float"],
                "volume_threshold": CONFIG["relative_volume_threshold"]
            },
            "alerts": [alert.to_dict() for alert in alerts]
        }
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Alerts exported to {filename}")
            
        return json.dumps(data, indent=2)
    
    @staticmethod
    def csv_export(alerts: List[StockAlert], filename: str = "alerts.csv"):
        """Export alerts to CSV for spreadsheet import."""
        import csv
        
        if not alerts:
            logger.info("No alerts to export to CSV")
            return
            
        headers = [
            "ticker", "price", "float", "relative_volume", "score",
            "has_news", "entry_low", "entry_high", "stop_loss", 
            "target_1", "target_2", "catalysts"
        ]
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            for alert in alerts:
                writer.writerow([
                    alert.ticker,
                    alert.price,
                    alert.float_shares,
                    alert.relative_volume,
                    alert.score,
                    alert.news_catalyst,
                    alert.entry_zone[0],
                    alert.entry_zone[1],
                    alert.stop_loss,
                    alert.target_1,
                    alert.target_2,
                    '|'.join(alert.catalyst_tags)
                ])
                
        logger.info(f"Alerts exported to {filename}")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """
    Main entry point for the stock screener.
    
    Usage:
        python stock_screener.py
        
    The scanner will:
    1. Connect to data sources
    2. Scan low-float stock universe
    3. Filter for volume spikes and news
    4. Output actionable alerts with entry/exit zones
    
    Configuration:
    - Edit CONFIG dictionary at top of file
    - Or set environment variables for API keys
    """
    
    # Check for API key from environment (optional for Yahoo fallback)
    api_key = os.environ.get("STOCK_API_KEY", CONFIG["api_key"])
    CONFIG["api_key"] = api_key
    
    print("\n" + "=" * 60)
    print("  LOW-FLOAT STOCK SCANNER FOR KOS")
    print("  Day Trading Opportunity Finder")
    print("=" * 60)
    print(f"  Max Price: ${CONFIG['max_price']}")
    print(f"  Max Float: {CONFIG['max_float']:,} shares")
    print(f"  Volume Threshold: {CONFIG['relative_volume_threshold']}x")
    print(f"  Min Alert Score: {CONFIG['min_alert_score']}/5")
    print("=" * 60 + "\n")
    
    # Initialize and run scanner
    scanner = StockScreener(CONFIG)
    alerts = scanner.scan()
    
    # Output results
    if CONFIG["output_format"] == "console":
        AlertOutput.console(alerts)
    
    # Always export to JSON for record keeping
    AlertOutput.json_export(alerts, "alerts.json")
    
    # Optional CSV export
    # AlertOutput.csv_export(alerts, "alerts.csv")
    
    return alerts


if __name__ == "__main__":
    import os
    main()
