import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
APIFY_TOKEN = os.environ["APIFY_TOKEN"]

DATASET_ID = "ใส่ Dataset ID ของ trn.th.mai6977"

url = f"https://api.apify.com/v2/datasets/{DATASET_ID}/items?token={APIFY_TOKEN}&format=json&clean=true"

data = requests.get(url).json()

if not isinstance(data, list):
    print(data)
    exit()

latest = data[0]
latest_video = latest.get("id")

with open("last_video.txt", "r") as f:
    old_video = f.read().strip()

if latest_video != old_video:
    video_url = latest.get("webVideoUrl", "")
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
