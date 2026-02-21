#!/usr/bin/env python3
"""
Autonomous Lead Scraper
Scrapes Product Hunt, Hacker News, and tech blogs for potential leads
"""
import json
import requests
import re
import datetime
from urllib.parse import urljoin

class LeadScraper:
    def __init__(self, db_path="/home/ubuntu/.openclaw/workspace/leadgen-service/leads-db.json"):
        self.db_path = db_path
        self.leads = self.load_leads()
        
    def load_leads(self):
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except:
            return {"leads": [], "metadata": {"total_leads": 0, "revenue_sol": 0}}
    
    def save_leads(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.leads, f, indent=2)
    
    def add_lead(self, company, contact, email, source, notes="", score=50):
        """Add a new lead to the database"""
        lead_id = f"lead_{int(datetime.datetime.now().timestamp())}"
        lead = {
            "id": lead_id,
            "company": company,
            "contact": contact,
            "email": email,
            "source": source,
            "notes": notes,
            "status": "New",
            "score": score,
            "created": datetime.datetime.now().isoformat(),
            "payment_status": "Pending",
            "emails_sent": 0,
            "last_contact": None
        }
        self.leads["leads"].append(lead)
        self.leads["metadata"]["total_leads"] = len(self.leads["leads"])
        self.save_leads()
        print(f"✅ Lead added: {company} - {email}")
        return lead
    
    def scrape_product_hunt(self):
        """Scrape Product Hunt for new products"""
        print("🔍 Scraping Product Hunt...")
        # Using public API
        try:
            # Get featured posts
            url = "https://www.producthunt.com/feed?category=featured"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            resp = requests.get(url, headers=headers, timeout=10)
            # Parse for product names and URLs
            # This is a simplified version - in production use proper RSS parsing
            print(f"Product Hunt feed fetched: {resp.status_code}")
            return []
        except Exception as e:
            print(f"Error scraping PH: {e}")
            return []
    
    def scrape_hacker_news(self):
        """Scrape Hacker News 'Show HN' posts"""
        print("🔍 Scraping Hacker News...")
        try:
            url = "https://hacker-news.firebaseio.com/v0/showstories.json"
            resp = requests.get(url, timeout=10)
            story_ids = resp.json()[:10]  # Top 10
            
            leads = []
            for story_id in story_ids:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story = requests.get(story_url, timeout=10).json()
                if story and 'title' in story:
                    # Extract potential company name from title
                    title = story.get('title', '')
                    url = story.get('url', '')
                    by = story.get('by', '')
                    
                    # Check if it's a product launch
                    if any(kw in title.lower() for kw in ['launch', 'show hn', 'introducing', 'announcing']):
                        lead = self.add_lead(
                            company=title[:50],
                            contact=f"HN User: {by}",
                            email="",  # Need to find email
                            source="HackerNews",
                            notes=f"URL: {url} | Score: {story.get('score', 0)}",
                            score=min(story.get('score', 0) / 10, 100)
                        )
                        leads.append(lead)
            return leads
        except Exception as e:
            print(f"Error scraping HN: {e}")
            return []
    
    def run(self):
        """Run full scraping cycle"""
        print(f"\n🚀 Starting lead scrape at {datetime.datetime.now()}")
        self.scrape_hacker_news()
        self.scrape_product_hunt()
        print(f"📊 Total leads in DB: {self.leads['metadata']['total_leads']}")
        self.save_leads()

if __name__ == "__main__":
    scraper = LeadScraper()
    scraper.run()
