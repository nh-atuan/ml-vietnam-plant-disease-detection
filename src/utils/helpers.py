import os
import logging

def setup_logger(name: str = "ml_system"):
    """Configures a basic logger for the project."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("project.log")
        ]
    )
    return logging.getLogger(name)

def get_project_root():
    """Returns absolute path to project root."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
