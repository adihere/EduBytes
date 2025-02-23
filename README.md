# EduBytes
EduBytes: AI-Powered Parent-to-Child Learning

EduBytes represents a paradigm shift in educational technology by empowering parents to co-create dynamic learning experiences with their children. 
This AI-driven platform combines multimodal content generation with adaptive learning mechanics to address critical gaps in modern education systems. 
By integrating parent insights, school curricula, and neurodiverse learning needs, EduBytes establishes a new standard for personalized education. 
This project also aims to bridge the gap between parental , school lessons and children's learning, making education more comprehensive and focused.

## Features
At its core is a Multimodal Content Generation Engine

- **Content Generation**: Creates educational content tailored to specific age groups
- **Video Creation**: Generates educational animations.
  -- For example: "Teach 8-year-old about equivalent fractions" triggers AI-generated animations showing pizza slices dividing progressively, with visual ratios maintained throughout transformations
- **Image Generation**: Produces relevant educational illustrations with text overlays
- **Audio Synthesis**: Converts text to age-appropriate speech
- **Interactive Elements**: Includes learning points and quiz questions

## Transformative Benefits for Modern Education
Democratizing Quality Instruction
EduBytes shatters geographic and socioeconomic barriers by enabling parents without formal teaching credentials to create expert-level content. 

Enhancing Teacher-Parent Collaboration
The platform's Shared Learning Dashboard (tbc) gives educators visibility into home learning activities, enabling targeted classroom reinforcement. 
When a student struggles with decimal operations in school, teachers can review home-generated content to identify conceptual gaps and suggest complementary EduBytes module

Multilayered Content Guardrails  (tbc)
EduBytes aims to integrate guardrails by leveraging tools such as Amazon Bedrock's security tools or similar 

Reusable Content Ecosystem  (tbc)
EduBytes plans to launch a GitHub-style repository where parents can:
Fork and Remix existing lessons 
Collaborative Development tools for multi-parent content creation team

Learning Byte Studio (tbc)
Teacher-focused interface for creating 3-5 minute review materials aligned with classroom lessons

## Prerequisites

- Python 3.8+
- API keys for:
  - Mistral AI
  - ElevenLabs
  - Fal.ai  

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/EduBytes.git
    cd EduBytes
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    Create a `.env` file in the root directory and add the following:
    ```env
    MISTRAL_API_KEY=your_mistral_api_key
    ELEVENLABS_API_KEY=your_elevenlabs_api_key
    FAL_KEY=your_fal_key    
    POSTHOG_KEY=your_posthog_key
    POSTHOG_URL=your_posthog_url
    ```

## Usage

1. Run the main application:
    ```sh
    python app/main.py
    ```

2. Launch the Gradio interface:
    ```sh
    python app/ui/gradio_interface.py
    ```

Access the web interface at `http://localhost:7860`

## Project Structure

```
EduBytes/
├── app/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── audio_agent.py
│   │   ├── content_agent.py
│   │   ├── image_agent.py
│   │   └── video_agent.py
│   ├── services/
│   │   └── __init__.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── interface.py
│   └── utils/
│       ├── __init__.py
│       ├── error_handling.py
│       ├── optimization.py
│       └── validators.py
├── tests/
│   └── __init__.py
├── .env
├── app.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License

## Testing

Run the tests using `unittest`:
```sh
python -m unittest discover tests
```
