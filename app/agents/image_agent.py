# agents/image_agent.py
from services.recraft import RecraftService
from PIL import Image, ImageDraw, ImageFont
import textwrap

class ImageAgent:
    def __init__(self):
        
        try:
            self.font = ImageFont.truetype("arial.ttf", 24)
        except IOError:
            self.font = ImageFont.load_default()        
            logger.warning("Arial font not found, using system default")

        self.service = RecraftService()
        self.font = ImageFont.truetype("arial.ttf", 24)
    
    def generate_images(self, text: str, age: int) -> list:
        keywords = self._extract_keywords(text)
        images = []
        for keyword in keywords[:30]:
            prompt = f"Educational illustration for {age} year olds about {keyword}"
            image_bytes = self.service.generate_image(prompt=prompt)
            annotated_img = self._add_text_overlay(image_bytes, keyword)
            images.append(annotated_img)
        return images

    def _add_text_overlay(self, image: bytes, text: str) -> Image:
        img = Image.open(io.BytesIO(image))
        draw = ImageDraw.Draw(img)
        text_lines = textwrap.wrap(text, width=20)
        y = 10
        for line in text_lines:
            draw.text((10, y), line, fill="white", font=self.font)
            y += 30
        return img
