# services/elevenlabs.py
from elevenlabs import generate, set_api_key
import os

class ElevenLabsService:
    def __init__(self):
        set_api_key(os.getenv("ELEVENLABS_API_KEY"))
    
    def text_to_speech(self, text: str, **kwargs) -> bytes:
        return generate(
            text=text,
            model="eleven_multilingual_v2",
            **kwargs
        )
