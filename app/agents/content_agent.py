# agents/content_agent.py
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from app.services.mistral import MistralService

class ContentAgent:
    def __init__(self):
        self.llm = MistralService().get_model()
        self.prompt_template = PromptTemplate(
            input_variables=["age", "prompt"],
            template="""Generate educational content for {age}-year-olds about: {prompt}
            Use simple language with concrete examples. Include 3 key learning points 
            and 2 interactive questions. Limit to 200-300 words."""
        )
    
    def generate_content(self, age: int, prompt: str) -> str:
        chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
        return chain.run(age=age, prompt=prompt)
