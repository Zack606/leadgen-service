#!/usr/bin/env python3
"""
Automated cold email outreach for new leads
"""
import json
import subprocess
import sys
from datetime import datetime

# Email templates
TEMPLATES = {
    "hn_startup": """Subject: Getting {company} in front of 50+ qualified buyers

Hi {contact},

Saw {company} on Hacker News today - congrats on the launch!

I run LeadGen Pro, a service that connects early-stage startups with decision-makers actively looking for solutions like yours.

Curious - are you currently exploring ways to get {company} in front of potential customers who are ready to buy?

If so, I can introduce you to 50+ qualified leads for just $50 worth of SOL.

Best,
Lucy
LeadGen Pro""",

    "ph_launch": """Subject: Your ProductHunt launch + distribution boost

Hi {contact},

Congratulations on the ProductHunt launch!

I'm reaching out because I help launched products like {company} connect with buyers who are actively searching for tools in your space.

Question: Are you looking for distribution channels beyond PH to acquire your first paying customers?

For $50 in SOL, I can deliver 50+ qualified leads who have budget and interest in {company}.

Interested?

Lucy""",

    "generic": """Subject: Lead generation for {company}

Hi {contact},

I came across {company} and wanted to reach out.

I specialize in connecting tech companies with qualified decision-makers. We help you find buyers who are actively looking for solutions in your space.

Would you be interested in 50 targeted leads for $50 (paid in SOL)?

Let me know if this makes sense for your growth goals.

Best,
Lucy
LeadGen Pro"""
}

def send_email(recipient, subject, body):
    """Send email using the send-email skill"""
    cmd = [
        "python3", 
        "/home/ubuntu/.openclaw/workspace/skills/send-email/send_email.py",
        recipient,
        subject,
        body
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except Exception as e:
        print(f"Email error: {e}")
        return False

def process_leads():
    """Process new leads and send outreach emails"""
    with open("/home/ubuntu/.openclaw/workspace/leadgen-service/leads-db.json", "r") as f:
        data = json.load(f)
    
    sent = 0
    for lead in data.get("leads", []):
        # Only email new leads with email addresses
        if lead.get("status") == "New" and lead.get("email") and lead.get("emails_sent", 0) == 0:
            
            # Pick template based on source
            source = lead.get("source", "")
            if "Hacker" in source:
                template = TEMPLATES["hn_startup"]
            elif "Product" in source:
                template = TEMPLATES["ph_launch"]
            else:
                template = TEMPLATES["generic"]
            
            # Format email
            email_body = template.format(
                company=lead.get("company", "your company"),
                contact=lead.get("contact", "there").split()[-1]  # Get last name or username
            )
            
            subject_line = email_body.split("\n")[0].replace("Subject: ", "")
            body = "\n".join(email_body.split("\n")[1:]).strip()
            
            print(f"Sending to {lead.get('email')}...")
            if send_email(lead.get("email"), subject_line, body):
                lead["status"] = "Contacted"
                lead["emails_sent"] = lead.get("emails_sent", 0) + 1
                lead["last_contact"] = datetime.now().isoformat()
                print(f"✅ Sent to {lead.get('company')}")
                sent += 1
            else:
                print(f"❌ Failed to send to {lead.get('email')}")
    
    # Save updates
    with open("/home/ubuntu/.openclaw/workspace/leadgen-service/leads-db.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"\n📧 Sent {sent} outreach emails")
    return sent

if __name__ == "__main__":
    sent = process_leads()
    sys.exit(0 if sent >= 0 else 1)
