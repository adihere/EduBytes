import os
import string
import random
from typing import Dict, List
from pathlib import Path
import shutil
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class OutputManager:
    OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'outputs')
    
    @staticmethod
    def generate_request_id(length: int = 12) -> str:
        """Generate a random alphanumeric request ID."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    @staticmethod
    def create_request_directory(request_id: str) -> Dict[str, str]:
        """Create directory structure for request outputs."""
        request_dir = os.path.join(OutputManager.OUTPUT_DIR, request_id)
        subdirs = ['text', 'audio', 'images', 'video']
        
        paths = {}
        for subdir in subdirs:
            full_path = os.path.join(request_dir, subdir)
            Path(full_path).mkdir(parents=True, exist_ok=True)
            paths[subdir] = full_path
            
        return paths
    
    @staticmethod
    def save_text_output(request_id: str, content: str) -> str:
        """Save text content to file."""
        output_path = os.path.join(OutputManager.OUTPUT_DIR, request_id, 'text', 'content.txt')
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Saved text content to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to save text content: {str(e)}")
            raise

    @staticmethod
    def save_audio_output(request_id: str, audio_data: bytes) -> str:
        """Save audio content to file."""
        if audio_data is None:
            logger.warning("No audio data received")
            return ""
            
        if not isinstance(audio_data, bytes):
            logger.error(f"Invalid audio data type: {type(audio_data)}")
            return ""
            
        output_path = os.path.join(OutputManager.OUTPUT_DIR, request_id, 'audio', 'audio.mp3')
        try:
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            logger.info(f"Saved audio content to {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Failed to save audio content: {str(e)}")
            return ""

    @staticmethod
    def save_images_output(request_id: str, images: List[Image.Image]) -> List[str]:
        """Save multiple images to files."""
        output_dir = os.path.join(OutputManager.OUTPUT_DIR, request_id, 'images')
        saved_paths = []
        try:
            for idx, image in enumerate(images):
                output_path = os.path.join(output_dir, f'image_{idx}.png')
                image.save(output_path, 'PNG')
                saved_paths.append(output_path)
            logger.info(f"Saved {len(saved_paths)} images to {output_dir}")
            return saved_paths
        except Exception as e:
            logger.error(f"Failed to save images: {str(e)}")
            raise

    @staticmethod
    def save_video_output(request_id: str, video_url: str) -> str:
        """Save video content from URL or copy from local path."""
        output_path = os.path.join(OutputManager.OUTPUT_DIR, request_id, 'video', 'video.mp4')
        try:
            if video_url.startswith(('http://', 'https://')):
                # For video URLs, you might want to implement download logic here
                # This is a placeholder for the actual implementation
                logger.info(f"Video URL saved: {video_url}")
                return video_url
            else:
                # For local files, copy to output directory
                shutil.copy2(video_url, output_path)
                logger.info(f"Saved video content to {output_path}")
                return output_path
        except Exception as e:
            logger.error(f"Failed to save video content: {str(e)}")
            raise

    @staticmethod
    def get_output_paths(request_id: str) -> Dict[str, str]:
        """Get all output paths for a specific request."""
        base_dir = os.path.join(OutputManager.OUTPUT_DIR, request_id)
        return {
            'text': os.path.join(base_dir, 'text', 'content.txt'),
            'audio': os.path.join(base_dir, 'audio', 'audio.mp3'),
            'images': os.path.join(base_dir, 'images'),
            'video': os.path.join(base_dir, 'video', 'video.mp4')
        }
