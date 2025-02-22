# utils/validators.py
import re
from typing import Dict, List, Union

class ContentValidator:
    @staticmethod
    def validate_prompt(prompt: str) -> Dict[str, Union[bool, List[str]]]:
        errors = []
        
        if not prompt:
            errors.append("Prompt cannot be empty")
        
        if len(prompt) > 250:
            errors.append("Prompt must be less than 250 characters")
            
        if len(prompt.split()) < 3:
            errors.append("Prompt must contain at least 3 words")
            
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def sanitize_input(text: str) -> str:
        # Remove potentially dangerous characters
        return re.sub(r'[<>"\'%;()&+]', '', text)