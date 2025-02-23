# app/services/fal_ai.py
import os
import logging
import fal_client
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class FalService:
    # Constants
    MAX_PROMPT_LENGTH = 2500

    def __init__(self):
        """Initialize the FAL service with API key from environment variables."""
        self.api_key = os.getenv('FAL_KEY')
        if not self.api_key:
            raise ValueError("FAL_KEY not found in environment variables")
        fal_client.api_key = self.api_key

    def _log_progress(self, update: Any) -> None:
        """Handle progress updates from fal-ai."""
        if isinstance(update, fal_client.InProgress):
            for log in update.logs:
                logger.info(f"Fal-AI Progress: {log['message']}")

    def _validate_and_truncate_prompt(self, prompt: str) -> str:
        """Validate and truncate prompt to meet API requirements."""
        if len(prompt) > self.MAX_PROMPT_LENGTH:
            logger.warning(f"Prompt exceeds max length ({len(prompt)}). Truncating to {self.MAX_PROMPT_LENGTH} characters.")
            return prompt[:self.MAX_PROMPT_LENGTH]
        return prompt

    def generate_video(self, prompt: str, duration: int = 5) -> str:
        """
        Generate a video based on the provided prompt.
        
        Args:
            prompt (str): Description of the video to generate
            duration (int): Video duration in seconds (default: 5)
            
        Returns:
            str: URL of the generated video
        """
        try:
            # Validate and truncate prompt
            prompt = self._validate_and_truncate_prompt(prompt)
            
            result = fal_client.subscribe(
                "fal-ai/kling-video/v1.6/standard/text-to-video",
                arguments={
                    "prompt": prompt,
                    "num_frames": duration * 30,  # 30fps
                    "resolution": "landscape_16_9"
                },
                with_logs=True,
                on_queue_update=self._log_progress
            )
            
            if isinstance(result, Dict) and 'video' in result and 'url' in result['video']:
                video_url = result['video']['url']
                logger.info(f"Video generated successfully: {video_url}")
                return video_url
            else:
                logger.error(f"Unexpected result format from video generation: {result}")
                raise ValueError(f"Invalid result format from video generation API")
                
        except Exception as e:
            logger.error(f"Video generation failed: {str(e)}")
            raise

    def generate_images(
        self,
        prompt: str,
        num_images: int = 1,
        seed: Optional[int] = None
    ) -> List[str]:
        """
        Generate images based on the provided prompt.
        
        Args:
            prompt (str): Description of the images to generate
            num_images (int): Number of images to generate (default: 1)
            seed (Optional[int]): Random seed for reproducibility
            
        Returns:
            List[str]: List of URLs for the generated images
        """
        try:
            result = fal_client.subscribe(
                "fal-ai/flux/dev",
                arguments={
                    "prompt": prompt,
                    "seed": seed,
                    "image_size": "landscape_4_3",
                    "num_images": num_images
                },
                with_logs=True,
                on_queue_update=self._log_progress
            )
            
            if isinstance(result, Dict) and 'images' in result:
                image_urls = [img['url'] for img in result['images']]
                logger.info(f"Successfully generated {len(image_urls)} images")
                return image_urls
            else:
                logger.error(f"Unexpected result format from image generation: {result}")
                raise ValueError(f"Invalid result format from image generation API")
                
        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            raise