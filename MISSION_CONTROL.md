# 🛰️ Braxton Helios Mission Control

**Mission:** Real-time market intelligence, alert generation, and social content automation.

---

## 📰 Newsroom

Fresh news feeds for premarket, midday, and after-hours scanning.

### Press Releases (Catalysts)
| Source | RSS URL | Status |
|--------|---------|--------|
| Business Wire | `https://feeds.businesswire.com/rss/default` | ⚠️ Testing |
| GlobeNewswire | `https://feeds.globenewswire.com/rss/default` | ⚠️ Testing |
| PR Newswire | `https://www.prnewswire.com/rss/` | ⚠️ Testing |
| Accesswire | `https://www.accesswire.com/rss/` | ⚠️ Testing |

### Perplexity AI - Subagent
| Status | Model | Description |
|--------|-------|-------------|
| ✅ Active | sonar-large-online | Real-time web search for news |

### SEC Filings
| Source | RSS URL | Status |
|--------|---------|--------|
| SEC EDGAR | `https://www.sec.gov/rss/edgar.xml` | ⚠️ Testing |

### Social Sentiment
| Source | URL | Type |
|--------|-----|------|
| StockTwits | `https://api.stocktwits.com/api/2/streams/trending.json` | API |

---

## 🎯 Daily Workflow

### 5:50 AM - Morning Research
1. **Use Perplexity subagent** for fresh news: "What are today's premarket movers?"
2. Fetch catalysts from Business Wire, SEC filings
3. Generate Morning Sentiment Report

### 11:22 AM - Midday Content
1. **Perplexity query:** "What's the biggest market moving news today?"
2. Scan midday movers
3. Generate midday update

### 4:55 PM - End-of-Day Wrap
1. **Perplexity query:** "What were the top after-hours movers today?"
2. Review catalysts
3. Generate EOD summary

---

## 📈 Data Sources

### Primary (Real-Time)
- Perplexity subagent (for fresh news queries)
- StockMarketWatch.com (premarket gapers)
- Business Wire (press releases)
- SEC EDGAR (filings)

### Secondary
- Yahoo Finance
- CNBC
- TradingView

---

## 🤖 Automation Notes

**Per as subplexity:** Useagent for natural language queries:
- "What are today's premarket movers?"
- "Find earnings beats from this morning"
- "What's the biggest market moving news?"

**RSS:** Still testing - some feeds may require API keys.

**Browser:** Can scrape directly from Benzinga, StockMarketWatch if needed.

---

## 📋 Templates

### Morning Sentiment Report
`morning-sentiment-template.md`

### Midday Update
See: Session notes

### Social Posts
Format: Ticker | Name (+%) → Headline → Key catalyst

---

*Last Updated: Feb 10, 2026*
*Status: ✅ Perplexity subagent active*
