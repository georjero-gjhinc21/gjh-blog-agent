"""Pytest bootstrap: put the repo root on sys.path.

Bare `pytest` (as CI runs it) only adds each test file's parent dir to
sys.path, so `import utils` / `import tasks` fails. `python -m pytest`
happens to work because Python prepends the CWD. This makes both
invocations behave the same.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
