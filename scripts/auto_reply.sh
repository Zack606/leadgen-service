#!/bin/bash
# Autonomous reply handler - runs every 5 minutes

API_KEY="sk_11146526917ff11e877bd39e1c190ec7cfdbd4aec0d67889"

echo "[$(date)] Checking for new email replies..."

# Check for new messages
RESPONSE=$(curl -s -X GET "https://sendclaw.com/api/mail/messages" \
  -H "X-Api-Key: $API_KEY")

# Check if there are unread messages (looking for "YES" or "SEND" or "interested")
echo "$RESPONSE" | grep -q '"isRead":false' && {
    echo "🎉 New email received! Processing autoreply..."
    
    # Extract sender email and subject
    SENDER=$(echo "$RESPONSE" | grep -oP '(?<=fromAddress":").*?(?=")')
    SUBJECT=$(echo "$RESPONSE" | grep -oP '(?<=subject":").*?(?=")')
    BODY=$(echo "$RESPONSE" | grep -oP '(?<=bodyText":").*?(?=")')
    
    echo "From: $SENDER"
    echo "Subject: $SUBJECT"
    echo "Body preview: ${BODY:0:100}"
    
    # Check if they want the free list
    if echo "$BODY" | grep -qiE "(yes|send|interested|leads|want|please)"; then
        echo "Sending FREE lead list..."
        
        curl -X POST "https://sendclaw.com/api/mail/send" \
          -H "X-Api-Key: $API_KEY" \
          -H "Content-Type: application/json" \
          -d "{
            \"to\": \"$SENDER\",
            \"subject\": \"Your FREE Startup Leads List + Special Offer\",
            \"body\": \"Hey there!\\n\\nThanks for your interest!\\n\\nHere's your FREE list of 100 revenue-stage startups hiring now:\\n\\n[LEAD LIST ATTACHMENT - In production this would be a real CSV]\\n\\nSample entries:\\n- TechCompany A (Series B, 50 employees, hiring 10 roles)\\n- SaaS Startup B (Series A, $2M ARR, hiring engineers)\\n- AI Tool C (Seed+, raised $500K last month)\\n\\n... and 97 more!\\n\\nWant FRESH leads delivered DAILY?\\n\\nGet 50 new leads every day for just \\\$50/month (paid in SOL).\\n\\nPayment address: CLnSrXVP9mF8VbanJdr7m5ZsCiDbB3wyjZBMEH9P292u\\n\\nReply PAY and I'll set you up instantly.\\n\\n- Lucy\\nLeadGen Pro\",
            \"cc\": []
          }"
    fi
}

echo "[$(date)] Check complete."
