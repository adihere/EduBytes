import os
from langchain_mistralai.chat_models import ChatMistralAI

class MistralService:
    def __init__(self):
        self.api_key = os.getenv('MISTRAL_API_KEY')
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment variables")
    
    def get_model(self):
        return ChatMistralAI(
            mistral_api_key=self.api_key,
            model="mistral-large-latest",   #Use latest model for educational content generation 
            temperature=0.7,
            max_tokens=2000
        )

    def generate_content(self, prompt: str) -> str:
        model = self.get_model()
        return model.predict(prompt)
