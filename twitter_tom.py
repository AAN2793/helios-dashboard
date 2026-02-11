#!/usr/bin/env python3
"""
Twitter Tom - Twitter/X News Sub-Agent
Monitors configured accounts and reports breaking news, unusual options, and stock alerts.
Reports to Helios in Wall Street Journal style - facts, no opinions.

Configured Accounts:
- Breaking News: @wallstengine, @StockMKTNewz, @DeItaone, @OracleNYSE, @TheInsiderPaper
- Unusual Options: @unusual_whales, @CheddarFlow
- Stock Alerts: @AlertsAndNews, @PlayBookTrades

API: TwitterAPI.io (pay-as-you-go, $0.15/1K tweets)
Uses advanced search with time windows to fetch only new tweets.
"""

import os
import time
import json
import requests
from datetime import datetime, timedelta

# TwitterAPI.io Configuration
TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY', 'new1_0ea7a1ec84574a33a4d8d903236960b8')
BASE_URL = 'https://api.twitterapi.io'

# Account Categories
ACCOUNTS = {
    'Breaking News': [
        '@wallstengine',
        '@StockMKTNewz', 
        '@DeItaone',
        '@OracleNYSE',
        '@TheInsiderPaper'
    ],
    'Unusual Options': [
        '@unusual_whales',
        '@CheddarFlow'
    ],
    'Stock Alerts': [
        '@AlertsAndNews',
        '@PlayBookTrades'
    ]
}

HEADERS = {'x-api-key': TWITTER_API_KEY}

# State file for tracking last check times
STATE_FILE = '/Users/helios/.openclaw/workspace/twitter_tom_state.json'

def load_state():
    """Load last check times from state file."""
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_state(state):
    """Save last check times to state file."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def fetch_new_tweets(username, since_time):
    """Fetch new tweets since the last check time."""
    url = f"{BASE_URL}/twitter/tweet/advanced_search"
    
    # Format times for API
    since_str = since_time.strftime("%Y-%m-%d_%H:%M:%S_UTC")
    until_str = datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S_UTC")
    
    # Build query - only get new tweets
    query = f"from:{username.replace('@', '')} since:{since_str} until:{until_str} include:nativeretweets"
    
    params = {
        "query": query,
        "queryType": "Latest"
    }
    
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=30)
        
        if response.status_code == 429:
            print(f"  {username}: Rate limited")
            return []
        
        if response.status_code != 200:
            print(f"  {username}: {response.status_code}")
            return []
        
        data = response.json()
        tweets = []
        
        # advanced_search returns tweets at root level
        for tweet in data.get('tweets', []):
            tweets.append({
                'text': tweet.get('text', ''),
                'id': tweet.get('id', ''),
                'created_at': tweet.get('createdAt', '')[:19].replace('T', ' '),
                'author': tweet.get('author', {}).get('userName', username.replace('@', '')),
                'retweet_count': tweet.get('retweetCount', 0),
                'like_count': tweet.get('likeCount', 0)
            })
        
        # Sort by time (oldest first - tweet order)
        tweets.reverse()
        
        print(f"  {username}: {len(tweets)} new tweets")
        return tweets
        
    except Exception as e:
        print(f"  {username}: Error - {e}")
        return []

def generate_report(all_reports):
    """Generate Wall Street Journal style report."""
    if not all_reports:
        return "No new news."
    
    lines = []
    lines.append(f"=== TWITTER TOM REPORT ===")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")
    
    for category, tweets in all_reports.items():
        if not tweets:
            continue
        lines.append(f"--- {category} ---")
        lines.append("")
        
        for tweet in tweets[:5]:  # Top 5 per category
            lines.append(f"{tweet['author']} | {tweet['created_at'][-8:]}")
            lines.append(f"{tweet['text'][:280]}")
            lines.append(f"RT: {tweet['retweet_count']} | LIKE: {tweet['like_count']}")
            lines.append("")
    
    lines.append("=== END REPORT ===")
    return '\n'.join(lines)

def run_twitter_tom():
    """Main execution for Twitter Tom."""
    print(f"\n{'='*50}")
    print(f"TWITTER TOM - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")
    
    # Load state
    state = load_state()
    now = datetime.utcnow()
    
    all_reports = {}
    
    for category, accounts in ACCOUNTS.items():
        print(f"[{category}]")
        category_tweets = []
        
        for account in accounts:
            username = account.replace('@', '')
            
            # Get last check time (default: 30 minutes ago)
            last_check = state.get(username)
            if last_check:
                since_time = datetime.fromisoformat(last_check.replace('Z', '+00:00'))
            else:
                since_time = now - timedelta(minutes=30)
            
            # Fetch new tweets
            tweets = fetch_new_tweets(account, since_time)
            category_tweets.extend(tweets)
            
            # Rate limiting: free tier 1 req/5 sec
            time.sleep(6)
        
        if category_tweets:
            all_reports[category] = category_tweets
        
        # Update state for each account
        state[username] = now.isoformat()
    
    # Save state
    save_state(state)
    
    # Generate report
    print(f"\n{'='*50}")
    print("REPORT")
    print(f"{'='*50}\n")
    
    report = generate_report(all_reports)
    print(report)
    
    # Save report
    report_file = '/Users/helios/.openclaw/workspace/twitter_tom_report.txt'
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\nSaved: {report_file}")
    
    return report

if __name__ == '__main__':
    run_twitter_tom()