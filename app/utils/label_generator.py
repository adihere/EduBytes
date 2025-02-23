import re
import logging
from typing import List
from app.services.mistral_tiny_service import MistralService

logger = logging.getLogger(__name__)

def generate_content_labels(prompt: str) -> List[str]:
    """Generate content labels using Mistral AI."""
    logger.info(f"Generating content labels for prompt: {prompt}")
    mistral_service = MistralService()
    content_labels = set()
    
    try:
        # Get hashtags using the correct method name
        content_labels = set(mistral_service.generate_hashtags(prompt))
        
        # If no hashtags found, try again with alternative prompt
        if not content_labels:
            logger.info("No hashtags found in initial response, attempting secondary generation")
            content_labels = set(mistral_service.retry_with_alternative_prompt(prompt))
        
        logger.info(f"Generated {len(content_labels)} unique hashtags")
        return list(content_labels)
        
    except Exception as e:
        logger.error(f"Error generating content labels: {str(e)}")
        return []
