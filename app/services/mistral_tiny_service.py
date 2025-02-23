import os
import logging
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.schema import HumanMessage, SystemMessage
from typing import List

logger = logging.getLogger(__name__)

class MistralService:
    def __init__(self):
        self.api_key = os.getenv('MISTRAL_API_KEY')
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment variables")
        self.model = self._get_model()

    def _get_model(self):
        return ChatMistralAI(
            mistral_api_key=self.api_key,
            model="mistral-large-latest",
            temperature=0.3,
            max_tokens=2000
        )

    def _create_system_prompt(self) -> str:
        return """You are an educational content tagger. Your task is to analyze educational content 
        and generate relevant hashtags. Each hashtag should be:
        1. A single word or compound word
        2. Prefixed with #
        3. Relevant to educational context
        4. No spaces within hashtags
        5. Focus on key educational concepts and subjects"""

    def generate_hashtags(self, content: str) -> List[str]:
        try:
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=self._create_system_prompt()),
                HumanMessage(content=f"Generate exactly 10 educational hashtags for this content:\n\n{content}")
            ])
            
            output_parser = CommaSeparatedListOutputParser()
            chain = prompt | self.model | output_parser
            
            hashtags = chain.invoke({"content": content})
            return [tag.strip() for tag in hashtags if tag.strip().startswith('#')][:10]

        except Exception as e:
            logger.error(f"Error generating hashtags: {str(e)}")
            return self.retry_with_alternative_prompt(content)

    def retry_with_alternative_prompt(self, content: str) -> List[str]:
        try:
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content=self._create_system_prompt()),
                HumanMessage(content=f"Extract 10 key educational concepts from this text and convert them into hashtags:\n\n{content}")
            ])
            
            output_parser = CommaSeparatedListOutputParser()
            chain = prompt | self.model | output_parser
            
            hashtags = chain.invoke({"content": content})
            return [f"#{tag.strip().replace('#', '')}" for tag in hashtags if tag.strip()][:10]

        except Exception as e:
            logger.error(f"Error in retry_with_alternative_prompt: {str(e)}")
            return []

    def generate_content(self, prompt: str) -> str:
        try:
            return self.model.predict(prompt)
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            raise
