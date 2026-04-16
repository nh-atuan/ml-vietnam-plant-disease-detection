import os
import logging
from pathlib import Path


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


def get_project_root() -> Path:
    """Return project root using __file__ (works in scripts and installed packages)."""
    return Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def find_project_root() -> Path:
    """Return project root by searching upward from cwd for src/ + notebooks/.

    Works in Jupyter notebooks where __file__ is not available.
    Falls back to get_project_root() if the directory structure is not found.
    """
    cwd = Path(os.getcwd())
    for candidate in [cwd, cwd.parent, cwd.parent.parent]:
        if (candidate / "src").exists() and (candidate / "notebooks").exists():
            return candidate
    return get_project_root()
