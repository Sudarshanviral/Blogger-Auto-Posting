import os
import requests
import datetime

CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["REFRESH_TOKEN"]
BLOG_ID = os.environ["BLOG_ID"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]


def get_access_token():
    r = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN,
            "grant_type": "refresh_token",
        },
    )
    return r.json()["access_token"]

def fetch_topic():
    url = f"https://newsapi.org/v2/top-headlines?country=us&pageSize=1&apiKey={NEWS_API_KEY}"
    return requests.get(url).json()["articles"][0]["title"]

def post_to_blogger(title):
    token = get_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = {
        "kind": "blogger#post",
        "title": title,
        "content": f"<p>Auto post on {datetime.datetime.utcnow()}</p>",
    }
    r = requests.post(url, headers=headers, json=body)
    print(r.text)

if __name__ == "__main__":
    topic = fetch_topic()
    post_to_blogger(topic)
