"""Test configuration: add backend/ to sys.path so the suite mirrors the
import style used by the application code (e.g. ``from models import ...``).
"""

import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))
