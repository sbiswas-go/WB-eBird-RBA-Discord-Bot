import requests
import os
from datetime import datetime

# Configuration 
EBIRD_API_KEY = os.environ.get('EBIRD_API_KEY')
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')
REGION_CODE = "IN-WB" 

def fetch_daily_notable_sightings():
    # Target the recent notable sightings endpoint
    url = f"https://api.ebird.org/v2/data/obs/{REGION_CODE}/recent/notable"
    headers = {"X-eBirdApiToken": EBIRD_API_KEY}
    
    # Query parameters: 'back=1' isolates sightings reported within the past 24 hours
    params = {"back": 1, "detail": "simple"}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to communicate with eBird API: Status {response.status_code}")
        return []

def format_and_post_to_discord(observations):
    if not observations:
        print("No new notable sightings reported in the last 24 hours.")
        return

    # Initialize a clean Markdown summary block
    date_str = datetime.now().strftime('%Y-%m-%d')
    # content = f" **Daily eBird Notable Sightings Alert: {REGION_CODE}** ({date_str}) \n\n"
    content = f" Daily eBird Notable Sightings Alert: {REGION_CODE} ({date_str}) \n\n"
    
    # Slice the results to avoid overrunning Discord's strict 2,000 character payload limits
    for obs in observations[:12]:
        com_name = obs.get("comName", "Unknown Species")
        sci_name = obs.get("sciName", "Unknown")
        loc_name = obs.get("locName", "Unknown Location")
        count = obs.get("howMany", "Unspecified")
        sub_id = obs.get("subId", "")
        
        # content += f"• **{com_name}** (*{sci_name}*) — Count: **{count}**\n"
        content += f"• {com_name} (*{sci_name}*) — Count: {count}\n"
        # content += f"  📍 Locality: *{loc_name}*\n"
        content += f"  📍 Locality: {loc_name}\n"
        if sub_id:
            # content += f"  🔗 [View eBird Checklist](https://ebird.org/checklist/{sub_id})\n"
            content += f"  🔗 <https://ebird.org/checklist/{sub_id}>\n"
        content += "\n"

    # Safe truncation fallback
    if len(content) > 2000:
        content = content[:1950] + "\n...Truncated due to character limits."

    payload = {"content": content}
    result = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    
    if result.status_code == 204:
        print("Alerts dispatched to Discord successfully.")
    else:
        print(f"Discord transfer failed: Status {result.status_code}, Response: {result.text}")

if __name__ == "__main__":
    sightings = fetch_daily_notable_sightings()
    format_and_post_to_discord(sightings)
