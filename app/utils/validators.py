# utils/validators.py
import re

class ContentValidator:
    MAX_WORDS = 250
    WORD_PATTERN = re.compile(r'\b\w+\b')
    
    @classmethod
    def validate_prompt(cls, text: str) -> dict:
        errors = []
        word_count = len(cls.WORD_PATTERN.findall(text))
        
        if word_count > cls.MAX_WORDS:
            errors.append(f"Prompt exceeds {cls.MAX_WORDS} words")
            
        if not text.strip():
            errors.append("Prompt cannot be empty")
            
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

    def sanitize_input(text: str) -> str:
        # Remove potentially dangerous characters
        return re.sub(r'[<>"\'%;()&+]', '', text)