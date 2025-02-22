from langchain_mistralai import ChatMistralAI
from langchain.schema import HumanMessage
from app.config import Config  # ensure Config is correctly imported
class MistralService:
    def __init__(self):
        self.client = ChatMistralAI(
            api_key=Config().mistral_key,
            model="mistral-large-latest",  # verify model identifier per docs
            temperature=0.7,
            max_tokens=2000
        )
    
    def generate_text(self, prompt: str) -> str:
        messages = [HumanMessage(content=prompt)]
        result = self.client.invoke(messages)  # use invoke method for chat models
        return result.content  # assuming the result object has a 'content' attribute
