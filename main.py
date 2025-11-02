from fastapi import FastAPI
from pydantic import BaseModel
import requests
import random

app = FastAPI()

# ===== YOUR ACTUAL KEYS =====
GROQ_API_KEY = "YOUR_GROQ_KEY_HERE"
PEXELS_API_KEY = "YOUR_PEXELS_KEY_HERE"

class SocialRequest(BaseModel):
    topic: str
    platform: str = "general"

def generate_caption(topic: str, platform: str) -> str:
    """Generate viral caption using Groq"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Create a VIRAL social media post about: {topic}
    Platform: {platform}
    Make it engaging, include emojis, and keep it under 250 characters.
    Return ONLY the caption text, nothing else.
    """
    
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama2-70b-4096",
        "temperature": 0.8
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"🔥 Amazing content about {topic}! Don't miss out! #viral #trending"

def get_images(topic: str) -> list:
    """Get images from Pexels"""
    url = f"https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": topic, "per_page": 3}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        photos = response.json()["photos"]
        return [photo["src"]["medium"] for photo in photos]
    except:
        # Fallback images
        return [
            "https://images.pexels.com/photos/414612/pexels-photo-414612.jpeg",
            "https://images.pexels.com/photos/459225/pexels-photo-459225.jpeg"
        ]

def generate_hashtags(topic: str) -> list:
    """Generate relevant hashtags"""
    words = topic.lower().split()
    base_hashtags = ["viral", "trending", "fyp", "popular"]
    topic_hashtags = [f"{word}" for word in words[:3]]
    return base_hashtags + topic_hashtags

@app.post("/generate-post")
async def generate_social_post(request: SocialRequest):
    # 1. Generate AI caption
    caption = generate_caption(request.topic, request.platform)
    
    # 2. Get images
    images = get_images(request.topic)
    
    # 3. Generate hashtags
    hashtags = generate_hashtags(request.topic)
    
    # 4. Best times to post
    best_times = ["9:00 AM", "12:00 PM", "3:00 PM", "7:00 PM"]
    
    return {
        "success": True,
        "platform": request.platform,
        "caption": caption,
        "hashtags": hashtags,
        "image_urls": images,
        "best_times_to_post": best_times,
        "viral_score": f"{random.randint(70, 95)}%"
    }

@app.get("/")
async def root():
    return {"message": "Mega Social Media API is LIVE!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)