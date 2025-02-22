# config.py
import os
import logging
from dotenv import load_dotenv
from typing import Optional

# Client and server settings
PORT_APP = 1116
SERVER_HOST = "0.0.0.0"

# UI settings
ICON_IMAGE_PATH = "./images/edubyte.gif"

class Config:
    def __init__(self):
        load_dotenv()
        
        # Application settings
        self.APP_NAME: str = "EduBytes"
        self.VERSION: str = "1.0.0"
        
        # API Keys
        self.mistral_key: Optional[str] = os.getenv("MISTRAL_API_KEY")
        self.elevenlabs_key: Optional[str] = os.getenv("ELEVENLABS_API_KEY")
        self.fal_key: Optional[str] = os.getenv("FAL_API_KEY")
        self.recraft_key: Optional[str] = os.getenv("RECRAFT_API_KEY")
        
        # Validate API keys
        self._validate_config()
        
        # Setup logging
        self._setup_logging()
    
    def _validate_config(self) -> None:
        missing_keys = []
        for key, value in {
            "MISTRAL_API_KEY": self.mistral_key,
            "ELEVENLABS_API_KEY": self.elevenlabs_key,
            "FAL_API_KEY": self.fal_key,
            "RECRAFT_API_KEY": self.recraft_key
        }.items():
            if not value:
                missing_keys.append(key)
        
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")
    
    def _setup_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('app.log'),
                logging.StreamHandler()
            ]
        )
