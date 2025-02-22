# utils/optimization.py
from functools import lru_cache
import concurrent.futures

class GenerationOptimizer:
    @lru_cache(maxsize=100)
    def cached_text_generation(self, prompt: str) -> str:
        return ContentAgent().generate_content(prompt)
    
    def parallel_image_generation(self, prompts: list) -> list:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            return list(executor.map(
                lambda p: ImageAgent().generate_image(p),
                prompts
            ))
