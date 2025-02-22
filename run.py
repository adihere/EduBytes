import os
import sys

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from app.ui.gradio_interface import create_interface

if __name__ == "__main__":
    demo = create_interface()
    demo.launch()
