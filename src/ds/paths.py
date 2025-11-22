from pathlib import Path

# Get the project root directory (assumes this file is in src/ds/)
# .../src/ds/paths.py -> .../src/ds -> .../src -> .../ (ROOT)
ROOT_DIR = Path(__file__).resolve().parents[2]

# Data directories
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    print(f"Project Root: {ROOT_DIR}")
    print(f"Raw Data: {RAW_DATA_DIR}")
