import logging
from app.services.fal_ai import FalService
from app.utils.output_manager import OutputManager

logger = logging.getLogger(__name__)

class VideoAgent:
    def __init__(self):
        self.service = FalService()
    
    def generate_video(self, text: str, age: int, request_id: str = None) -> str:
        try:
            prompt = f"""Create a 5-second educational animation for {age}-year-olds 
            illustrating: {text}"""
            
            # Generate video and get URL
            video_url = self.service.generate_video(
                prompt=prompt,
                duration=5
            )
            
            # If we have a request_id, save the video URL
            if request_id:
                video_path = OutputManager.save_video_output(request_id, video_url)
                logger.info(f"Video saved for request {request_id}: {video_path}")
                return video_path
            
            return video_url
            
        except Exception as e:
            logger.error(f"Failed to generate video: {str(e)}")
            raise
