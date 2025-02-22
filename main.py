import os
import logging
from dotenv import load_dotenv

from app.ui.interface import create_interface

from app.config import Config, PORT_APP

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )

def main():
    # Load environment variables
    load_dotenv()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize config
        config = Config()
        
        # Create and launch the Gradio interface
        demo = create_interface()
        demo.launch(
            server_name="0.0.0.0", 
            server_port=PORT_APP,
            share=True  # Enable sharing via public URL
        )
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
        raise

if __name__ == "__main__":
    main()
