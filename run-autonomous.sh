#!/bin/bash
# Autonomous Lead Generation & Money Making System
# Run this on startup via cron

echo "[$(date)] Starting LeadGen Pro autonomous cycle..."

# Step 1: Scrape Hacker News for new startups
echo "[$(date)] Scraping Hacker News..."
cd /home/ubuntu/.openclaw/workspace/leadgen-service
python3 scripts/scraper.py >> logs/scraper.log 2>&1

# Step 2: Sync new leads to Notion
echo "[$(date)] Syncing to Notion..."
python3 scripts/notion_sync.py >> logs/notion.log 2>&1

# Step 3: Send cold emails to new leads
echo "[$(date)] Sending cold emails..."
python3 scripts/cold_email_outreach.py >> logs/email.log 2>&1

# Step 4: Check Solana wallet for payments
echo "[$(date)] Checking wallet..."
# We can addSolana balance check here later

echo "[$(date)] Cycle complete."
