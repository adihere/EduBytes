# agents/video_agent.py
from app.services.fal_ai import FalService

class VideoAgent:
    def __init__(self):
        self.service = FalService()
    
    def generate_video(self, text: str, age: int) -> str:
        prompt = f"""Create a 5-second educational animation for {age}-year-olds 
        illustrating: {text}"""
        return self.service.generate_video(
            prompt=prompt,
            duration=5,
            model="kling-1.6-pro",
            resolution="1024x576"
        )
