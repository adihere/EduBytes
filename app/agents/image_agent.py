import io
import logging
from typing import List
from PIL import Image, ImageDraw, ImageFont
import textwrap
import requests
from app.services.fal_ai import FalService

NUMBER_OF_IMAGES = 5

logger = logging.getLogger(__name__)

class ImageAgent:
    def __init__(self):
        self.service = FalService()
        try:
            self.font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            logger.warning("Arial font not found, using system default")
            self.font = ImageFont.load_default()

    def _extract_keywords(self, text: str) -> List[str]:
        # Simple keyword extraction - split by spaces and take unique words
        words = set(text.lower().split())
        # Remove common stop words (you might want to expand this list)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to'}
        return list(words - stop_words)

    def generate_images(self, text: str, age: int) -> List[Image.Image]:
        try:
            keywords = self._extract_keywords(text)
            images = []
            
            for keyword in keywords[:5]:
                prompt = f"Educational illustration for {age} year olds about {keyword}, digital art style, cute and friendly, colorful"
                try:
                    # Get image URLs from FalService
                    image_urls = self.service.generate_images(
                        prompt=prompt,
                        num_images=1
                    )
                    
                    # Download and process each image
                    for url in image_urls:
                        response = requests.get(url)
                        image = Image.open(io.BytesIO(response.content))
                        annotated_img = self._add_text_overlay(image, keyword)
                        images.append(annotated_img)
                        
                except Exception as e:
                    logger.error(f"Failed to generate image for keyword '{keyword}': {str(e)}")
                    continue
            
            if not images:
                raise Exception("Failed to generate any images")
            
            return images
            
        except Exception as e:
            logger.error(f"Error in image generation process: {str(e)}")
            raise

    def _add_text_overlay(self, image: Image.Image, text: str) -> Image.Image:
        draw = ImageDraw.Draw(image)
        text_lines = textwrap.wrap(text, width=20)
        y = 10
        for line in text_lines:
            draw.text((10, y), line, fill="white", font=self.font)
            y += 30
        return image

