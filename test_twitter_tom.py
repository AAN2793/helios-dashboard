#!/usr/bin/env python3
"""Quick test for Twitter Tom."""

import os
import requests
from datetime import datetime

TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY', 'new1_0ea7a1ec84574a33a4d8d903236960b8')
BASE_URL = 'https://api.twitterapi.io'
HEADERS = {'x-api-key': TWITTER_API_KEY}

def fetch_user_tweets(username, max_results=5):
    """Fetch latest tweets from a Twitter user."""
    url = f"{BASE_URL}/twitter/user/last_tweets"
    params = {'userName': username.replace('@', ''), 'limit': max_results}
    
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Error: {response.text[:200]}")
            return []
        
        data = response.json()
        tweets = []
        for tweet in data.get('tweets', []):
            tweets.append({
                'text': tweet.get('text', '')[:280],
                'created_at': tweet.get('createdAt', '')[:19].replace('T', ' '),
                'retweet_count': tweet.get('retweetCount', 0),
                'like_count': tweet.get('likeCount', 0),
                'author': tweet.get('author', {}).get('userName', username),
            })
        
        return tweets
        
    except Exception as e:
        print(f"Error: {e}")
        return []

# Test with DeItaone
print(f"Testing @DeItaone at {datetime.now().strftime('%H:%M:%S')}")
tweets = fetch_user_tweets('@DeItaone', max_results=5)
print(f"\nGot {len(tweets)} tweets:\n")

for tweet in tweets:
    print(f"[{tweet['created_at'][-5:]}] @{tweet['author']}")
    print(f"{tweet['text'][:200]}...")
    print(f"RT: {tweet['retweet_count']} | LIKE: {tweet['like_count']}")
    print("-" * 40)