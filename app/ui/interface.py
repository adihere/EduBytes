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
from app.utils.label_generator import generate_content_labels  # Add this import

# Define custom CSS before the interface creation
custom_css = """
    .gradio-container {    
        font-family: "Georgia", serif;
    }
    
    .gradio-title {
        font-family: "Quicksand", sans-serif;
        color: #2a4494;
        text-align: center;
        margin-bottom: 1em;
    }
    
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }

    .small-accordion .gr-accordion-header {
        font-size: 0.8em;
        padding: 0.5em;
    }

.small-accordion .gr-accordion-body {
    padding: 0.5em;
}
    
    .banner-image {
        display: block;
        margin: 0 auto;
        max-width: 100%;
        height: auto;
    }
    
    .input-row {
        margin: 20px 0;
    }
    
    .button-primary {
        background-color: #2a4494;
        color: white;
    }
    
    .status-box {
        border: 1px solid #eee;
        padding: 10px;
        margin: 5px 0;
        border-radius: 4px;
    }
    
    .content-output {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
    }
"""

logger = logging.getLogger(__name__)
error_handler = ErrorHandler()

def start_generation_workflow(age: int, prompt: str, video_needed: bool = False, images_needed: bool = False) -> List[Any]:
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
        
        # Generate content labels before saving content
        content_labels = generate_content_labels(content)
        logger.info(f"Generated content labels: {content_labels}")
        
        # Append content labels to the content before saving
        formatted_labels = "\n\nLabels: " + ", ".join(content_labels)
        content_with_labels = content + formatted_labels
        
        content_path = OutputManager.save_text_output(request_id, content_with_labels)
        progress["content"] = "Content generated successfully"
        
        # Conditionally generate images using content labels
        images = []
        image_paths = []
        if images_needed:
            progress["images"] = "Generating images..."
            image_agent = ImageAgent()
            images = error_handler.api_call_with_retry(
                image_agent.generate_images,
                content, 
                age,
                content_labels  # Pass the labels to image agent
            )
            image_paths = OutputManager.save_images_output(request_id, images)
            progress["images"] = f"Images generated successfully and saved to {output_paths['images']}"
        else:
            progress["images"] = "Image generation skipped"

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

        # Store all media in a single list
        media_files = []
        
        # Add images if generated
        if images and image_paths:
            media_files.extend(image_paths)
            progress["images"] = f"Images generated successfully"
        
        # Add video if generated
        if video_needed:
            video_agent = VideoAgent()
            video = error_handler.api_call_with_retry(
                video_agent.generate_video,
                content, 
                age,
                request_id
            )
            video_path = OutputManager.save_video_output(request_id, video)
            if video_path:
                media_files.append(video_path)
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
            gr.update(value=media_files),  # Combined media files
        ]
        
    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        return [gr.update(value=f"Error: {str(ve)}")] * 7  # Updated count
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return [gr.update(value="An unexpected error occurred")] * 7  # Updated count

def create_interface():
    with gr.Blocks(
        title="Educational Content Generator",
        css=custom_css,
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="purple",
        )
    ) as demo:        

        with gr.Row(equal_height=True, elem_classes="banner-container"):
            gr.Image(
                value="./app/images/edubyte2.jpeg",  # Add the image path
                show_label=False,
                height=150,
                width=150,
                show_download_button=False,
                container=False,
                elem_classes="banner-image"
            )
        gr.Markdown("## EduBytes: Revolutionizing Parent-Child Learning Through AI-Powered Personalization")
        
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
            images_checkbox = gr.Checkbox(
                label="Generate Images",
                value=True,
                info="Generate educational illustrations"
            )
        
        submit_btn = gr.Button("Generate Content", variant="primary")
        
        with gr.Accordion("Generation Progress", open=True, elem_classes="small-accordion"):
            with gr.Row():
                text_status = gr.Textbox(label="Content Generation", interactive=False)
                audio_status = gr.Textbox(label="Audio Generation", interactive=False)
                image_status = gr.Textbox(label="Image Generation", interactive=False)
                video_status = gr.Textbox(label="Video Generation", interactive=False)

        with gr.Accordion("Generated Content", open=True):
            content_output = gr.Textbox(label="Generated Learning Text", interactive=False)
            audio_output = gr.Audio(label="Audio Bytes", interactive=False)
            # Combined gallery for images and video
            media_output = gr.Gallery(
                label="Generated Media",
                show_label=True,
                elem_id="media_gallery",
                columns=[2],
                rows=[2],
                height="auto",
                allow_preview=True,
                show_share_button=False,
                show_download_button=True,
            )

        submit_btn.click(
            fn=start_generation_workflow,
            inputs=[age_dropdown, prompt_input, video_checkbox, images_checkbox],
            outputs=[
                text_status, audio_status, image_status, video_status,
                content_output, audio_output, media_output
            ]
        )
    
    return demo