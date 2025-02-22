import os
import requests

class RecraftService:
    def __init__(self):
        self.api_key = os.getenv('RECRAFT_API_KEY')
        if not self.api_key:
            raise ValueError("RECRAFT_API_KEY not found in environment variables")
        self.api_url = "https://api.recraft.ai/v1/generate"
    
    def generate_image(self, prompt: str) -> bytes:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": prompt,
            "style": "educational",
            "format": "png"
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.content
