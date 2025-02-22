# services/mistral.py
from langchain_community.llms import MistralAI

class MistralService:
    def __init__(self):
        self.client = MistralAI(
            api_key=Config().mistral_key,
            model="mistral-7b",
            temperature=0.7,
            max_tokens=2000
        )
    
    def generate_text(self, prompt: str) -> str:
        return self.client(prompt)
