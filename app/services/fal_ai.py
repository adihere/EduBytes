import os
from fal.toolkit import ImageGenerator

class FalService:
    def __init__(self):
        self.api_key = os.getenv('FAL_API_KEY')
        if not self.api_key:
            raise ValueError("FAL_API_KEY not found in environment variables")
    
    def generate_video(self, prompt: str, duration: int = 5, model: str = "stable-diffusion", resolution: str = "1024x576") -> str:
        generator = ImageGenerator(
            api_key=self.api_key,
            model_name=model
        )
        return generator.generate_video(
            prompt=prompt,
            duration=duration,
            resolution=resolution
        )
