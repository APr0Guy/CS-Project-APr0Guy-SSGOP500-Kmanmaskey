from pathlib import Path
import sys


def resource_path(relative_path):
    """Return an absolute path to a bundled asset or a source-project asset."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent

    return str(base_path / relative_path)
