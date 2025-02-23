import logging
from app.services.elevenlabs import ElevenLabsService

logger = logging.getLogger(__name__)

class AudioAgent:
    def __init__(self):
        self.service = ElevenLabsService()
    
    def generate_audio(self, text: str, age: int) -> str:
        try:
            # Ensure age is an integer
            age = int(age)
            voice_params = self._select_voice_profile(age)
            return self.service.text_to_speech(
                text=text,
                voice=voice_params['name'],
                stability=voice_params['stability'],
                similarity_boost=voice_params['similarity']
            )
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid age parameter: {e}")
            raise TypeError(f"Age must be an integer, got {type(age)}: {age}")
        except Exception as e:
            logger.error(f"Error generating audio: {e}")
            raise

    def _select_voice_profile(self, age: int) -> dict:
        age_groups = {
            (3,6): {'name': 'Child', 'stability': 0.7, 'similarity': 0.8},
            (7,12): {'name': 'Teen', 'stability': 0.8, 'similarity': 0.75},
            (13,16): {'name': 'Adult', 'stability': 0.9, 'similarity': 0.7}
        }
        return next(v for k,v in age_groups.items() if k[0] <= age <= k[1])
