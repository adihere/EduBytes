# ui/gradio_interface.py
import gradio as gr
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

def start_generation_workflow(age: int, prompt: str):
    validate = ContentValidator.validate_prompt(prompt)
    if not validate["valid"]:
        raise gr.Error(", ".join(validate["errors"]))
    
    content = ContentAgent().generate_content(age, prompt)
    audio = AudioAgent().generate_audio(content, age)
    images = ImageAgent().generate_images(content, age)
    video = VideoAgent().generate_video(content, age)
    
    return [
        gr.Textbox(value="Content generated", visible=True),
        gr.Audio(audio, visible=True),
        gr.Gallery(images, visible=True),
        gr.Video(video, visible=True)
    ]


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
