import os
import requests

# Setze hier deine Client-ID und OAuth-Token ein
client_id = os.getenv("TW_CLIENT_ID", None)
token = os.getenv("TW_TOKEN", None)


url = f"https://api.twitch.tv/helix/clips?broadcaster_id={206130928}&started_at=2023-11-01T00:00:00Z"
headers = {"Client-ID": client_id, "Authorization": f"Bearer {token}"}
#resp = requests.get(url, headers=headers).json()
resp2 = requests.get(url, headers=headers)
#print(resp)

limit = resp2.headers.get("Ratelimit-Limit")
remaining = resp2.headers.get("Ratelimit-Remaining")
reset_time = resp2.headers.get("Ratelimit-Reset")

print(f"Limit: {limit}")
print(f"Remaining: {remaining}")
print(f"Reset Time: {reset_time}")