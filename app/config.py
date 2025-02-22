# config.py
import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        APP_NAME = "EduBytes"
        VERSION = "1.0.0"
        load_dotenv()
        self.mistral_key = os.getenv("MISTRAL_API_KEY")
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.fal_key = os.getenv("FAL_API_KEY")
        self.recraft_key = os.getenv("RECRAFT_API_KEY")

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app.log'),
                logging.StreamHandler()
            ]
        )
