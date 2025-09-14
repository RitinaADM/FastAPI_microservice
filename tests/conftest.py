import sys
from pathlib import Path

# Add src directory to Python path so tests can import modules correctly
project_root = Path(__file__).parent.parent  # This goes up to ritina_app directory
src_path = project_root / "src"

# Add src path to sys.path so we can import modules as if they were top-level
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))