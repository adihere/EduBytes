# EduBytes
EduBytes: AI-Powered Parent-to-Child Learning

EduBytes is an innovative educational platform that empowers parents to create engaging, personalized learning experiences for their children using the power of AI. 
This project aims to bridge the gap between parental , school lessons and children's learning, making education more comprehensive and focused.

Key Features
Parent Input: Parents provide a brief text description of the topic they want their child to learn.
AI-Generated Content: The app uses advanced AI to transform the parent's input into a comprehensive 2-minute audio-visual tutorial.
Multimodal Output: The tutorial combines clear concept explanations, voiceover narration, and relevant images or short videos.
Interactive Quiz: Each tutorial concludes with a brief 3-question quiz to reinforce learning and assess understanding.

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

Quiz Creation:
The AI generates three pertinent questions based on the tutorial content.
Questions are designed to be age-appropriate and reinforce key learning points.

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
