import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
APIFY_TOKEN = os.environ["APIFY_TOKEN"]

print("TOKEN START =", APIFY_TOKEN[:12])
print("TOKEN LENGTH =", len(APIFY_TOKEN))

DATASET_ID = "GQcLvQyOqnakvhw0E"

print("DATASET_ID =", DATASET_ID)

url = f"https://api.apify.com/v2/datasets/{DATASET_ID}/items?token={APIFY_TOKEN}&format=json&clean=true"

print("URL =", url.replace(APIFY_TOKEN, "***"))

data = requests.get(url).json()

print("DATA =", data)

if not isinstance(data, list):
    print(data)
    exit()

if not data:
    print("No data")
    exit()

latest = data[0]
latest_video = latest.get("id")

with open("last_video.txt", "r") as f:
    old_video = f.read().strip()

if latest_video != old_video:
    video_url = latest.get("webVideoUrl", "https://www.tiktok.com/@trn.th.mai6977")
    text = latest.get("text", "")

    message = f"🎉 คลิปใหม่จาก TikTok\n\nช่อง: @trn.th.mai6977\n{text}\n\n{video_url}"

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

    with open("last_video.txt", "w") as f:
        f.write(latest_video)

    print("New video detected")
else:
    print("No new video")
