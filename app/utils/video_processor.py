import logging
import moviepy.editor as mp
from typing import List, Optional
from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

logger = logging.getLogger(__name__)

class VideoProcessor:
    @staticmethod
    def create_multimodal_video(
        output_path: str,
        text: str,
        audio_path: Optional[str],
        images: List[Image.Image],
        video_path: Optional[str] = None,
        duration: int = 30
    ) -> str:
        try:
            # Save images temporarily
            temp_image_paths = []
            for i, img in enumerate(images):
                temp_path = f"temp_image_{i}.png"
                img.save(temp_path)
                temp_image_paths.append(temp_path)

            # Create clips from images
            image_clips = [
                mp.ImageClip(img_path).set_duration(duration / len(images))
                for img_path in temp_image_paths
            ]

            # Create text overlay
            text_clip = (mp.TextClip(
                text,
                fontsize=24,
                color='white',
                bg_color='rgba(0,0,0,0.5)',
                size=(600, None)
            ).set_duration(duration))

            # Initialize base clip
            if video_path and os.path.exists(video_path):
                base_clip = mp.VideoFileClip(video_path)
            else:
                # If no video, concatenate image clips
                base_clip = mp.concatenate_videoclips(image_clips)

            # Combine elements
            final_clip = mp.CompositeVideoClip([
                base_clip,
                text_clip.set_position(('center', 'bottom'))
            ])

            # Add audio if available
            if audio_path and os.path.exists(audio_path):
                audio_clip = mp.AudioFileClip(audio_path)
                final_clip = final_clip.set_audio(audio_clip)

            # Write final video
            final_clip.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac'
            )

            # Cleanup temporary files
            for temp_path in temp_image_paths:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

            return output_path

        except Exception as e:
            logger.error(f"Error creating multimodal video: {str(e)}")
            raise
        finally:
            # Ensure cleanup of temporary files
            for temp_path in temp_image_paths:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
