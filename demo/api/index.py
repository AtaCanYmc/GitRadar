import os
import sys
from pathlib import Path

# Add demo directory to sys.path so bundled gitradar package is importable on Vercel
DEMO_DIR = Path(__file__).parent.parent
if str(DEMO_DIR) not in sys.path:
    sys.path.insert(0, str(DEMO_DIR))

# Import monkeypatch for Python compatibility
import gitradar  # noqa: F401
from gitradar.web.app import create_app

app = create_app()
