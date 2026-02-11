# HELIOS Setup Game Plan
## Step-by-Step Configuration Guide

---

## 🎯 PHASE 1: Brave Search API (Free Web Search)

### Step 1.1: Get Your Brave API Key
1. Go to **https://brave.com/search/api/**
2. Click "Get API Key" or "Sign Up"
3. Create account (free tier = 2,000 queries/month)
4. Copy your API key

### Step 1.2: Configure OpenClaw
Run this command in terminal:
```bash
openclaw configure --section web
```

When prompted, enter:
- **Brave API Key:** [paste what you got from Step 1.1]

### Step 1.3: Test It
After config, I can search like:
- "AMD earnings today"
- "premarket movers February 4 2026"
- "overnight stock news"

---

## 📧 PHASE 2: Gmail Access (Evening Email Checks)

### Step 2.1: Set Up Google OAuth
1. Go to **Google Cloud Console**: https://console.cloud.google.com/
2. Create new project (name: "Helios OpenClaw")
3. Enable **Gmail API**
4. Create OAuth 2.0 credentials
5. Download credentials JSON

### Step 2.2: Configure OpenClaw
Run:
```bash
openclaw configure --section gmail
```

Or set environment variable:
```bash
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"
```

### Step 2.3: Authorize
First run will open browser for Google sign-in and consent screen.

---

## 🔄 PHASE 3: Test & Optimize

### After Both Set Up, I'll Be Able To:
- ✅ Search overnight news at 5:50 AM
- ✅ Check emails during evening heartbeat (7-9 PM)
- ✅ Build newsletter with current data
- ✅ Find runners from Benzinga/Trade Ideas via browser

---

## 📋 QUICK REFERENCE COMMANDS

```bash
# Configure Brave Search
openclaw configure --section web

# Configure Gmail
openclaw configure --section gmail

# Check current config (what's set)
openclaw config.get

# Restart gateway after config changes
openclaw gateway restart
```

---

## ⚠️ NOTES

- **Free Brave tier:** 2,000 queries/month = ~67 searches/day (plenty for our use)
- **Gmail:** Uses OAuth, no app passwords needed
- **Cost:** Both can run on free tiers
- **Next:** After this, we tackle X/Twitter posting (~$100/mo) or manual posting

---

## ✅ CHECKLIST

- [ ] Get Brave API key from brave.com/search/api
- [ ] Run `openclaw configure --section web`
- [ ] Test web search capability
- [ ] Set up Google Cloud project for Gmail
- [ ] Enable Gmail API in Google Cloud
- [ ] Create OAuth credentials
- [ ] Run `openclaw configure --section gmail`
- [ ] Authorize via browser
- [ ] Test evening email check

---

**Ready when you are! Start with Phase 1 around 10 AM.**