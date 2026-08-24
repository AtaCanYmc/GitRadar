import os
import sys
from pathlib import Path

# Insert repository root directory into Python path
ROOT_DIR = Path(__file__).parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import monkeypatch for Python compatibility
import gitradar  # noqa: F401
from gitradar.web.app import create_app

app = create_app()
