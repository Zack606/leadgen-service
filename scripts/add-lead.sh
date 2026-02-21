#!/bin/bash
# Add a new lead to the database
# Usage: ./add-lead.sh "Company Name" "Contact" "Email" "Source" "Notes"

LEADS_FILE="/home/ubuntu/.openclaw/workspace/leadgen-service/leads-db.json"
COMPANY="$1"
CONTACT="$2"
EMAIL="$3"
SOURCE="$4"
NOTES="$5"

if [ -z "$COMPANY" ]; then
    echo "Usage: $0 \"Company\" \"Contact\" \"Email\" \"Source\" \"Notes\""
    exit 1
fi

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
LEAD_ID="lead_$(date +%s)"

# Create the lead entry
LEAD_JSON=$(cat <<EOF
{
    "id": "$LEAD_ID",
    "company": "$COMPANY",
    "contact": "$CONTACT",
    "email": "$EMAIL",
    "source": "$SOURCE",
    "notes": "$NOTES",
    "status": "new",
    "score": 0,
    "created_at": "$TIMESTAMP",
    "updated_at": "$TIMESTAMP",
    "paid": false
}
EOF
)

# For now, just append to a simple log
echo "[$TIMESTAMP] New Lead: $COMPANY | $CONTACT <$EMAIL> | Source: $SOURCE" >> /home/ubuntu/.openclaw/workspace/leadgen-service/data/leads/leads.log

echo "✅ Lead recorded: $COMPANY - $CONTACT"
