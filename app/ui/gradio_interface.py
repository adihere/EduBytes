# ui/gradio_interface.py
import gradio as gr
import logging
from typing import List, Any
from app.utils.validators import ContentValidator
from app.agents.content_agent import ContentAgent
from app.agents.image_agent import ImageAgent
from app.agents.video_agent import VideoAgent
from services.mistral import generate_content
from services.elevenlabs import text_to_speech
from services.recraft import generate_image
from services.fal_ai import generate_video

import os
from posthog import Posthog

# POSTHOG_KEY is stored in environment variables
posthog_key = os.getenv('POSTHOG_KEY')
posthog_url = os.getenv('POSTHOG_URL')
posthog = Posthog(posthog_key, host=posthog_url)

logger = logging.getLogger(__name__)

def start_generation_workflow(age: int, prompt: str) -> List[Any]:
    try:
        # Validate input
        validation = ContentValidator.validate_prompt(prompt)
        if not validation["valid"]:
            raise ValueError(", ".join(validation["errors"]))
        
        # Initialize progress
        progress = {
            "content": "Starting content generation...",
            "images": "Waiting...",
            "video": "Waiting...",
            "audio": "Waiting..."
        }
        
        # Generate content
        content_agent = ContentAgent()
        content = content_agent.generate_content(age, prompt)
        progress["content"] = "Content generated successfully"
        progress["images"] = "Generating images..."
        
        # Generate images
        image_agent = ImageAgent()
        images = image_agent.generate_images(content, age)
        progress["images"] = "Images generated successfully"
        progress["video"] = "Generating video..."
        
        # Generate video
        video_agent = VideoAgent()
        video = video_agent.generate_video(content, age)
        progress["video"] = "Video generated successfully"
        
        return [
            gr.update(value=progress["content"]),
            gr.update(value=progress["images"]),
            gr.update(value=progress["video"]),
            gr.update(value=content),
            gr.update(value=images),
            gr.update(value=video)
        ]
        
    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        return [gr.update(value=f"Error: {str(ve)}")] * 6
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return [gr.update(value="An unexpected error occurred")] * 6

def create_interface():
    with gr.Blocks(title="EduContent Generator") as demo:
        gr.Markdown("## AI-Powered Educational Content Creator")
        
        with gr.Row():
            age_dropdown = gr.Dropdown(
                label="Target Age",
                choices=[str(i) for i in range(3, 17)],
                value="10"
            )
            prompt_input = gr.Textbox(
                label="Lesson Prompt",
                max_length=250,
                placeholder="Enter educational content prompt to guide the AI agents to create video (max 250 words)"
            )
        
        submit_btn = gr.Button("Generate Content", variant="primary")
        
        with gr.Accordion("Generation Progress", open=False):
            text_status = gr.Textbox(label="Content Generation", interactive=False)
            audio_status = gr.Textbox(label="Audio Generation", interactive=False)
            image_status = gr.Textbox(label="Image Generation", interactive=False)
            video_status = gr.Textbox(label="Video Generation", interactive=False)

        submit_btn.click(
            fn=start_generation_workflow,
            inputs=[age_dropdown, prompt_input],
            outputs=[text_status, audio_status, image_status, video_status]
        )
    return demo
