# EduBytes
EduBytes: AI-Powered Parent-to-Child Learning

EduBytes is an innovative educational platform that empowers parents to create engaging, personalized learning experiences for their children using the power of AI. 
This project aims to bridge the gap between parental , school lessons and children's learning, making education more comprehensive and focused.

Key Features
Parent Input: Parents provide a brief text description of the topic they want their child to learn.
AI-Generated Content: The app uses advanced AI to transform the parent's input into a comprehensive 2-minute audio-visual tutorial.
Multimodal Output: The tutorial combines clear concept explanations, voiceover narration, and relevant images or short videos.

Future Roadmap
Interactive Quiz: Each tutorial concludes with a brief 3-question quiz to reinforce learning and assess understanding.
Quiz Creation:
The AI generates three pertinent questions based on the tutorial content.
Questions are designed to be age-appropriate and reinforce key learning points.

Library of educational videos for re-use


How It Works
Content Generation:
An AI agent analyzes the parent's input and generates a concise, age-appropriate tutorial script.
The script is optimized for a 2-minute delivery, focusing on key concepts and examples.

Visual Enhancement:
Another AI module searches for and selects relevant images or short video clips to accompany the audio.
The visuals are timed to sync with the narration, enhancing understanding and engagement.

Audio Production:
Text-to-speech technology converts the script into clear, natural-sounding narration.
Background music or sound effects may be added to increase appeal.


Final Assembly:
All components are brought together into a seamless 2-minute audio-visual presentation.
The quiz is appended to the end of the tutorial.

## Folder Structure

```
project_root/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── gradio_interface.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── video_agent.py
│   │   ├── image_agent.py
│   │   └── content_agent.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── fal_ai.py
│   │   ├── recraft.py
│   │   ├── mistral.py
│   │   └── elevenlabs.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── models/
│   └── mistral-7b/
├── data/
│   ├── raw/
│   ├── processed/
│   └── output/
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   └── test_services.py
├── notebooks/
├── docs/
├── scripts/
│   └── setup.py
├── .gitignore
├── requirements.txt
└── README.md
```

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

## Testing

Run the tests using `unittest`:
```sh
python -m unittest discover tests
```
