#!/bin/bash

# Initialize variables
bot_token=""
webhook_url=""
secret_token=""

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -t) bot_token="$2"; shift ;;
        -u) webhook_url="$2"; shift ;;
        -s) secret_token="$2"; shift ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Check if all parameters are provided
if [[ -z "$bot_token" || -z "$webhook_url" || -z "$secret_token" ]]; then
    echo "Error: All parameters (-t, -u, -s) are required."
    echo "Usage: $0 -t <value> -u <value> -s <value>"
    exit 1
fi

# Set the webhook
curl -X POST "https://api.telegram.org/bot$bot_token/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{
           "url": "'"$webhook_url"'",
           "secret_token": "'"$secret_token"'"
         }'