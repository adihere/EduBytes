import io
import logging
from typing import List
from PIL import Image, ImageDraw, ImageFont
import textwrap
from app.services.recraft import RecraftService

logger = logging.getLogger(__name__)

class ImageAgent:
    def __init__(self):
        self.service = RecraftService()
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
            for keyword in keywords[:5]:  # Limit to 5 images for performance
                prompt = f"Educational illustration for {age} year olds about {keyword}"
                image_bytes = self.service.generate_image(prompt=prompt)
                annotated_img = self._add_text_overlay(image_bytes, keyword)
                images.append(annotated_img)
            return images
        except Exception as e:
            logger.error(f"Error generating images: {str(e)}")
            raise

    def _add_text_overlay(self, image: bytes, text: str) -> Image:
        img = Image.open(io.BytesIO(image))
        draw = ImageDraw.Draw(img)
        text_lines = textwrap.wrap(text, width=20)
        y = 10
        for line in text_lines:
            draw.text((10, y), line, fill="white", font=self.font)
            y += 30
        return img
