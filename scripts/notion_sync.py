#!/usr/bin/env python3
"""
Sync leads between local JSON and Notion database
"""
import json
import requests
import os
import sys

NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "30ec826d-55a4-816d-a9e0-e690ad092d60")

def add_to_notion(lead):
    """Add a lead to the Notion database"""
    if not NOTION_API_KEY:
        print("No Notion API key configured")
        return None
    
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    email = lead.get("email")
    email_payload = {"email": email} if email else {"email": None}
    
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": lead.get("company", "Unknown")}}]},
            "Company": {"rich_text": [{"text": {"content": lead.get("company", "")}}]},
            "Contact": {"rich_text": [{"text": {"content": lead.get("contact", "")}}]},
            "Source": {"select": {"name": lead.get("source", "Scraped")}},
            "Status": {"select": {"name": lead.get("status", "New")}},
            "Score": {"number": lead.get("score", 50)},
            "Created": {"date": {"start": lead.get("created", "2026-02-21")}}
        }
    }
    
    # Only add email if present
    if email:
        data["properties"]["Email"] = {"email": email}
    
    resp = requests.post(url, headers=headers, json=data)
    if resp.status_code == 200:
        print(f"✅ Added to Notion: {lead.get('company')}")
        return resp.json().get("id")
    else:
        print(f"❌ Failed to add: {resp.text[:200]}")
        return None

def main():
    db_path = "/home/ubuntu/.openclaw/workspace/leadgen-service/leads-db.json"
    
    try:
        with open(db_path, "r") as f:
            data = json.load(f)
    except:
        print("No leads to sync")
        return
    
    synced = 0
    for lead in data.get("leads", []):
        if not lead.get("notion_id"):
            notion_id = add_to_notion(lead)
            if notion_id:
                lead["notion_id"] = notion_id
                synced += 1
    
    with open(db_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Synced {synced} leads to Notion")

if __name__ == "__main__":
    main()
