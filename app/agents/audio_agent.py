# agents/audio_agent.py
from app.services.elevenlabs import ElevenLabsService

class AudioAgent:
    def __init__(self):
        self.service = ElevenLabsService()
    
    def generate_audio(self, text: str, age: int) -> str:
        voice_params = self._select_voice_profile(age)
        return self.service.text_to_speech(
            text=text,
            voice=voice_params['name'],
            stability=voice_params['stability'],
            similarity_boost=voice_params['similarity']
        )

    def _select_voice_profile(self, age: int) -> dict:
        age_groups = {
            (3,6): {'name': 'Child', 'stability': 0.7, 'similarity': 0.8},
            (7,12): {'name': 'Teen', 'stability': 0.8, 'similarity': 0.75},
            (13,16): {'name': 'Adult', 'stability': 0.9, 'similarity': 0.7}
        }
        return next(v for k,v in age_groups.items() if k[0] <= age <= k[1])
