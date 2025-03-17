import requests
import json
import os

# Google OAuth Credentials (GitHub Secrets me save karein)
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
BLOG_ID = os.getenv("BLOG_ID")

# Function to get new access token
def get_access_token():
    url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token")

# Function to fetch trending topics (Google News API se)
def fetch_trending_topics():
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return [article["title"] for article in articles[:5]]

# Function to generate AI-written blog content (Gemini API)
def generate_ai_blog(topic):
    ai_api_key = os.getenv("GEMINI_API_KEY")
    headers = {"Authorization": f"Bearer {ai_api_key}", "Content-Type": "application/json"}
    data = {"model": "gemini-1.0", "prompt": f"Write a blog post about {topic}"}
    response = requests.post("https://generativelanguage.googleapis.com/v1beta/models/generateText", headers=headers, json=data)
    return response.json().get("candidates", [{}])[0].get("output", "AI content generation failed.")

# Function to post on Blogger
def post_to_blogger(title, content):
    access_token = get_access_token()
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    post_data = {"kind": "blogger#post", "title": title, "content": content}
    response = requests.post(url, headers=headers, json=post_data)
    
    if response.status_code == 200:
        print(f"✅ Blog Posted: {title}")
    else:
        print(f"❌ Error: {response.text}")

# Main function to run automation
def run_auto_posting():
    topics = fetch_trending_topics()
    for topic in topics:
        ai_content = generate_ai_blog(topic)
        post_to_blogger(topic, ai_content)

# Run the function
if __name__ == "__main__":
    run_auto_posting()
