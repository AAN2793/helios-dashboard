#!/usr/bin/env python3
"""
@AlertsAndNews Social Content Generator
Generates copy-paste ready posts for X/Twitter and Stocktwits.

Usage:
    python alerts_content_generator.py --ticker TSLA --action breakout --price 420 --context "holding support"
    python alerts_content_generator.py --ticker NVDA --action alert --price 140 --change +5.2%
"""

import argparse
import random
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class StockAlert:
    ticker: str
    action: str  # breakout, breakdown, alert, runner, dip
    price: float
    change_pct: Optional[float] = None
    context: Optional[str] = None
    volume_spike: Optional[str] = None  # e.g., "2.5x avg"
    target: Optional[float] = None
    support: Optional[float] = None


class ContentGenerator:
    """Generate social media content for trading alerts."""

    # Templates organized by action type
    TEMPLATES = {
        "breakout": [
            "🚀 ${ticker} BREAKOUT! Breaking above ${price} with {volume} volume. Next target: ${target} 🎯",
            "⚡ ${ticker} launching! ${price} resistance shattered. Momentum building for ${target} 🚀",
            "🔥 ${ticker} through ${price}! When this breaks out, it RUNS. Watching ${target} next 📈",
        ],
        "runner": [
            "🏃‍♂️ ${ticker} RUNNER ALERT! Up {change} to ${price}. {volume} volume - this has legs!",
            "🔥 EARLY RUNNER: ${ticker} moving fast. ${price} with unusual flow. Get it on watch NOW!",
            "⚡ ${ticker} catching bids at ${price}. {context}. Volume screaming RUNNER! 🏃‍♂️",
        ],
        "alert": [
            "👀 ${ticker} ALERT: Trading at ${price}. {context}. On watch for continuation!",
            "🎯 ${ticker} setting up at ${price}. {volume} volume. Key level: ${support} 🔑",
            "⚠️ ${ticker} watchlist alert. ${price} with {context}. Flow starting to pick up 👀",
        ],
        "dip": [
            "💰 ${ticker} DIP BUY opportunity at ${price}. Down {change} - oversold bounce play?",
            "🎣 ${ticker} pulling back to ${price}. Strong support at ${support}. Loading zone? 💪",
            "📉 ${ticker} -{change} from highs. Now ${price}. Weak hands shaking out. Bounce watch 👀",
        ],
        "breakdown": [
            "⚠️ ${ticker} BREAKDOWN! Lost ${price} support. Next stop ${target}?",
            "🔻 ${ticker} cracking ${price}. {volume} volume to downside. Caution here ⚠️",
        ],
        "institutional": [
            "🏦 SMART MONEY: {institution} loading ${ticker} at ${price}. ${amount} position. Follow the 💰",
            "🐋 ${ticker} whale alert. {institution} just disclosed {amount} stake at ~${price}. 👀",
        ],
    }

    STOCKTWITS_TEMPLATES = {
        "breakout": [
            "${ticker} BREAKOUT 📈 Breaking ${price} with {volume} vol. Target: ${target} | bullish",
            "${ticker} breakout play ${price} → ${target}. Momentum building | long",
            "${ticker} through ${price} resistance. Watching ${target} next 🚀 | breakout",
        ],
        "runner": [
            "${ticker} RUNNER 🏃‍♂️ {change} to ${price}. {volume}. Still moving | momentum",
            "${ticker} early runner alert. ${price} unusual volume 👀 | watchlist",
            "${ticker} catching steam at ${price}. Volume flowing in | runner",
        ],
        "alert": [
            "${ticker} ALERT 👀 ${price} with {context}. On the radar | swingtrade",
            "${ticker} setup at ${price}. Key lvl ${support} 🔑 | daytrade",
        ],
    }

    HASHSETS = {
        "default": ["#stocks", "#trading", "#daytrade", "#stockmarket"],
        "meme": ["#memestocks", "#wallstreetbets", "#yolo", "#stocks"],
        "tech": ["#techstocks", "#nasdaq", "#tradingsignals", "#stocks"],
        "smallcap": ["#smallcaps", "#pennystocks", "#lowfloat", "#runner"],
    }

    def __init__(self):
        self.used_templates = set()

    def generate_x_post(self, alert: StockAlert, template_key: Optional[str] = None) -> str:
        """Generate X/Twitter post."""
        if template_key is None:
            template_key = alert.action

        templates = self.TEMPLATES.get(template_key, self.TEMPLATES["alert"])
        template = random.choice(templates)
        self.used_templates.add(template)

        # Format the template
        content = template.format(
            ticker=alert.ticker.upper(),
            price=f"{alert.price:.2f}" if alert.price else "N/A",
            change=f"{alert.change_pct:+.1f}%" if alert.change_pct else "N/A",
            target=f"{alert.target:.2f}" if alert.target else "???",
            support=f"{alert.support:.2f}" if alert.support else "support",
            volume=alert.volume_spike if alert.volume_spike else "elevated",
            context=alert.context if alert.context else "unusual activity",
        )

        # Add hashtags (80% of posts)
        if random.random() > 0.2:
            hashset = self._choose_hashset(alert.ticker)
            content += "\n" + " ".join(random.sample(hashset, 2))

        return content

    def generate_stocktwits_post(self, alert: StockAlert) -> str:
        """Generate Stocktwits post (shorter, different format)."""
        templates = self.STOCKTWITS_TEMPLATES.get(
            alert.action, self.STOCKTWITS_TEMPLATES["alert"]
        )
        template = random.choice(templates)

        content = template.format(
            ticker=alert.ticker.upper(),
            price=f"{alert.price:.2f}" if alert.price else "N/A",
            change=f"{alert.change_pct:+.1f}%" if alert.change_pct else "N/A",
            target=f"{alert.target:.2f}" if alert.target else "???",
            support=f"{alert.support:.2f}" if alert.support else "support",
            volume=alert.volume_spike if alert.volume_spike else "volume",
            context=alert.context if alert.context else "activity",
        )
        return content

    def generate_variations(self, alert: StockAlert, count: int = 3) -> dict:
        """Generate multiple variations for A/B testing or choice."""
        variations = {
            "x_posts": [],
            "stocktwits_posts": [],
        }

        for _ in range(count):
            variations["x_posts"].append(self.generate_x_post(alert))
            variations["stocktwits_posts"].append(self.generate_stocktwits_post(alert))

        return variations

    def _choose_hashset(self, ticker: str) -> List[str]:
        """Choose appropriate hashtag set based on ticker characteristics."""
        # Meme stocks
        meme_tickers = ["GME", "AMC", "BB", "PLTR", "HOOD", "RIVN", "LCID"]
        if ticker.upper() in meme_tickers:
            return self.HASHSETS["meme"]

        # Tech giants
        tech_tickers = ["AAPL", "NVDA", "MSFT", "GOOGL", "META", "TSLA", "AMZN"]
        if ticker.upper() in tech_tickers:
            return self.HASHSETS["tech"]

        return self.HASHSETS["default"]

    def generate_batch_alerts(self, tickers_data: List[dict]) -> dict:
        """Generate alerts for multiple tickers."""
        results = {}
        for data in tickers_data:
            alert = StockAlert(**data)
            results[alert.ticker] = self.generate_variations(alert)
        return results


def main():
    parser = argparse.ArgumentParser(description="Generate trading alert content")
    parser.add_argument("--ticker", required=True, help="Stock ticker")
    parser.add_argument("--action", default="alert", choices=["breakout", "runner", "alert", "dip", "breakdown", "institutional"])
    parser.add_argument("--price", type=float, required=True, help="Current price")
    parser.add_argument("--change", type=float, help="Percent change")
    parser.add_argument("--context", help="Additional context")
    parser.add_argument("--target", type=float, help="Target price")
    parser.add_argument("--support", type=float, help="Support level")
    parser.add_argument("--variations", type=int, default=3, help="Number of variations")

    args = parser.parse_args()

    alert = StockAlert(
        ticker=args.ticker,
        action=args.action,
        price=args.price,
        change_pct=args.change,
        context=args.context,
        target=args.target,
        support=args.support,
    )

    generator = ContentGenerator()
    variations = generator.generate_variations(alert, count=args.variations)

    print(f"\n{'='*60}")
    print(f"🎯 GENERATED CONTENT FOR ${args.ticker.upper()}")
    print(f"{'='*60}\n")

    print("🐦 X/TWITTER OPTIONS:")
    print("-" * 40)
    for i, post in enumerate(variations["x_posts"], 1):
        print(f"\n{i}. {post}\n")

    print("\n📊 STOCKTWITS OPTIONS:")
    print("-" * 40)
    for i, post in enumerate(variations["stocktwits_posts"], 1):
        print(f"\n{i}. {post}\n")

    print(f"{'='*60}")
    print("Copy-paste ready. Use the one that fits best!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
