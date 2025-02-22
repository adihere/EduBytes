# services/elevenlabs.py
import os
from elevenlabs import generate, set_api_key

class ElevenLabsService:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
        set_api_key(self.api_key)
    
    def text_to_speech(self, text: str, voice: str = "Josh", stability: float = 0.5, similarity_boost: float = 0.5) -> bytes:
        return generate(
            text=text,
            voice=voice,
            model="eleven_monolingual_v1",
            stability=stability,
            similarity_boost=similarity_boost
        )
