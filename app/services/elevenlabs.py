# services/elevenlabs.py
import os
from elevenlabs.client import ElevenLabs

class ElevenLabsService:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables")
        self.client = ElevenLabs(api_key=self.api_key)
    
    def text_to_speech(self, text: str, voice: str = "Josh", stability: float = 0.5, similarity_boost: float = 0.5) -> bytes:
        try:
            # Get available voices
            voices_response = self.client.voices.get_all()
            voices = voices_response.voices  # Access the 'voices' attribute
            
            # Find the requested voice or use the first available one
            selected_voice = next(
                (v for v in voices if v.name.lower() == voice.lower()), 
                voices[0] if voices else None
            )
            
            if not selected_voice:
                raise ValueError(f"Voice '{voice}' not found and no default voice available")
            
            # Generate audio using the selected voice 
             
            audio_generator = self.client.text_to_speech.convert(
                text=text,
                voice_id=selected_voice.voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )
            
        except Exception as e:
            raise Exception(f"Text-to-speech generation failed: {str(e)}")