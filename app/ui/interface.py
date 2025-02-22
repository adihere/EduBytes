import gradio as gr
import logging
from typing import List, Any
from app.utils.validators import ContentValidator
from app.agents.content_agent import ContentAgent
from app.agents.image_agent import ImageAgent
from app.agents.video_agent import VideoAgent
from app.agents.audio_agent import AudioAgent
from app.utils.error_handling import ErrorHandler

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()

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
        
        # Generate content using error handler
        content_agent = ContentAgent()
        content = error_handler.api_call_with_retry(
            content_agent.generate_content,
            age, 
            prompt
        )
        progress["content"] = "Content generated successfully"
        progress["images"] = "Generating images..."
        
        # Generate images
        image_agent = ImageAgent()
        images = error_handler.api_call_with_retry(
            image_agent.generate_images,
            content, 
            age
        )
        progress["images"] = "Images generated successfully"
        progress["video"] = "Generating video..."
        
        # Generate video
        video_agent = VideoAgent()
        video = error_handler.api_call_with_retry(
            video_agent.generate_video,
            content, 
            age
        )
        progress["video"] = "Video generated successfully"
        
        # Generate audio
        audio_agent = AudioAgent()
        audio = error_handler.api_call_with_retry(
            audio_agent.generate_audio,
            content, 
            age
        )
        progress["audio"] = "Audio generated successfully"
        
        return [
            gr.update(value=progress["content"]),
            gr.update(value=progress["audio"]),
            gr.update(value=progress["images"]),
            gr.update(value=progress["video"]),
            gr.update(value=content),
            gr.update(value=audio),
            gr.update(value=images),
            gr.update(value=video)
        ]
        
    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        return [gr.update(value=f"Error: {str(ve)}")] * 8
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return [gr.update(value="An unexpected error occurred")] * 8

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
                placeholder="Enter educational content prompt (max 250 characters)"
            )
        
        submit_btn = gr.Button("Generate Content", variant="primary")
        
        with gr.Accordion("Generation Progress", open=True):
            text_status = gr.Textbox(label="Content Generation", interactive=False)
            audio_status = gr.Textbox(label="Audio Generation", interactive=False)
            image_status = gr.Textbox(label="Image Generation", interactive=False)
            video_status = gr.Textbox(label="Video Generation", interactive=False)
        
        with gr.Accordion("Generated Content", open=True):
            content_output = gr.Textbox(label="Generated Text", interactive=False)
            audio_output = gr.Audio(label="Generated Audio")
            image_output = gr.Gallery(label="Generated Images")
            video_output = gr.Video(label="Generated Video")

        submit_btn.click(
            fn=start_generation_workflow,
            inputs=[age_dropdown, prompt_input],
            outputs=[
                text_status, audio_status, image_status, video_status,
                content_output, audio_output, image_output, video_output
            ]
        )
    
    return demo
