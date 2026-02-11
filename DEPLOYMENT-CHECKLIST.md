# 📋 Deployment Checklist for Kos

**Do this AFTER your morning session (before your flight at noon)**

---

## Step 1: Open Terminal
- Press `Cmd + Space` → type "Terminal" → Enter

## Step 2: Run These Commands (Copy/Paste Each Line)

```bash
cd ~/.openclaw/workspace/orphan-well-dashboard
```

```bash
git init
```

```bash
git add .
```

```bash
git commit -m "Initial commit"
```

```bash
gh repo create orphan-well-dashboard --public --source=. --remote=origin
```

*(If it asks for credentials, just press Enter)*

```bash
git push -u origin main
```

## Step 3: Deploy on Vercel

1. Go to **vercel.com** and sign in
2. Click **"Add New..."** → **"Project"**
3. Find **"orphan-well-dashboard"** in the list
4. Click **"Import"**
5. Click **"Deploy"**

## Step 4: Get Your Link

Vercel will show a success page with your URL:
```
https://orphan-well-dashboard.vercel.app
```

Bookmark it on your phone!

---

## What You'll See

✅ Orphan Well Analysis Tool
✅ Market Dashboard
✅ Activity Log
✅ Flight Status (AA873)
✅ Settings

---

## If GitHub Asks for Auth

If `gh repo create` fails, do this:

1. Go to **github.com** → Sign in
2. Click **"+"** → **"New repository"**
3. Name: `orphan-well-dashboard`
4. Set to **Public**
5. Click **"Create repository"**
6. Then run:
```bash
git remote add origin https://github.com/AAN2793/orphan-well-dashboard.git
git push -u origin main
```

---

## Need Help?

Text me and I'll walk you through it. 👍