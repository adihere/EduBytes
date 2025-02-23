import gradio as gr
import logging
from typing import List, Any
from app.utils.validators import ContentValidator
from app.agents.content_agent import ContentAgent
from app.agents.image_agent import ImageAgent
from app.agents.video_agent import VideoAgent
from app.agents.audio_agent import AudioAgent
from app.utils.error_handling import ErrorHandler
from app.utils.output_manager import OutputManager

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()

def start_generation_workflow(age: int, prompt: str, video_needed: bool = False) -> List[Any]:
    try:
        # Convert age to integer
        age = int(age)
        
        # Generate request ID and create output directories
        request_id = OutputManager.generate_request_id()
        output_paths = OutputManager.create_request_directory(request_id)
        logger.info(f"Starting generation workflow with request ID: {request_id}, video generation: {video_needed}")
        
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
        content_path = OutputManager.save_text_output(request_id, content)
        progress["content"] = "Content generated successfully"
        progress["images"] = "Generating images..."
        
        # Generate images
        image_agent = ImageAgent()
        images = error_handler.api_call_with_retry(
            image_agent.generate_images,
            content, 
            age
        )
        image_paths = OutputManager.save_images_output(request_id, images)
        progress["images"] = f"Images generated successfully and saved to {output_paths['images']}"
        progress["video"] = "Generating video..."
        
        # Generate audio and save it
        audio_agent = AudioAgent()
        audio = error_handler.api_call_with_retry(
            audio_agent.generate_audio,
            content, 
            age
        )
        
        if audio is None:
            progress["audio"] = "Audio generation failed"
            audio_path = ""
        else:
            audio_path = OutputManager.save_audio_output(request_id, audio)
            if audio_path:
                progress["audio"] = f"Audio generated successfully and saved to {output_paths['audio']}"
            else:
                progress["audio"] = "Failed to save audio output"

        # Conditionally generate video with request_id
        video = None
        if video_needed:
            video_agent = VideoAgent()
            video = error_handler.api_call_with_retry(
                video_agent.generate_video,
                content, 
                age,
                request_id
            )
            progress["video"] = "Video generated successfully"
        else:
            progress["video"] = "Video generation skipped"
            
        logger.info(f"Completed generation workflow for request ID: {request_id}")
        
        return [
            gr.update(value=progress["content"]),
            gr.update(value=progress["audio"]),
            gr.update(value=progress["images"]),
            gr.update(value=progress["video"]),
            gr.update(value=content),
            gr.update(value=audio_path if audio_path else None),  # Only return path if valid
            gr.update(value=image_paths),
            gr.update(value=video if video_needed else None)
        ]
        
    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        return [gr.update(value=f"Error: {str(ve)}")] * 8
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return [gr.update(value="An unexpected error occurred")] * 8

def create_interface():
    with gr.Blocks(title="Educational Content Generator") as demo:
        gr.Markdown("## AI-Powered Educational Content Creator")
        
        with gr.Row():
            age_dropdown = gr.Dropdown(
                label="Target Age",
                choices=[str(i) for i in range(3, 17)],
                value="10",
                type="value"  # Changed from "number" to "value"
            )
            prompt_input = gr.Textbox(
                label="Lesson Prompt",
                max_length=250,
                placeholder="Enter educational content prompt (max 250 characters)"
            )
            
        with gr.Row():
            video_checkbox = gr.Checkbox(
                label="Generate Video",
                value=False,
                info="Generate a short educational video (takes longer)"
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
            inputs=[age_dropdown, prompt_input, video_checkbox],
            outputs=[
                text_status, audio_status, image_status, video_status,
                content_output, audio_output, image_output, video_output
            ]
        )
    
    return demo
