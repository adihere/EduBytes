# EduBytes
EduBytes: AI-Powered Parent-to-Child Learning

EduBytes is an innovative educational platform that empowers parents to create engaging, personalized learning experiences for their children using the power of AI. 
This project aims to bridge the gap between parental , school lessons and children's learning, making education more comprehensive and focused.

## Features

- **Content Generation**: Creates educational content tailored to specific age groups
- **Video Creation**: Generates educational animations
- **Image Generation**: Produces relevant educational illustrations with text overlays
- **Audio Synthesis**: Converts text to age-appropriate speech
- **Interactive Elements**: Includes learning points and quiz questions

## Prerequisites

- Python 3.8+
- API keys for:
  - Mistral AI
  - ElevenLabs
  - Fal.ai
  - Recraft.ai

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
    FAL_API_KEY=your_fal_api_key
    RECRAFT_API_KEY=your_recraft_api_key
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
│   ├── agents/           # AI agents for different content types
│   ├── services/         # External API integrations
│   └── ui/              # User interface components
├── app.py               # Main application entry point
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
