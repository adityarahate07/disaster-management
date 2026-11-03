import os
import sys

# Limit OpenBLAS threads to conserve memory in serverless environments
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

# Ensure root and app directories are in sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
APP_DIR = os.path.join(ROOT_DIR, "app")

for p in [ROOT_DIR, APP_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Setup NLTK data directory for serverless environment
import nltk
nltk_data_dir = os.environ.get("NLTK_DATA", "/tmp/nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)
if nltk_data_dir not in nltk.data.path:
    nltk.data.path.insert(0, nltk_data_dir)

# Ensure required tokenizers/lemmatizers exist
for package in ["punkt", "punkt_tab", "wordnet"]:
    try:
        nltk.download(package, download_dir=nltk_data_dir, quiet=True)
    except Exception:
        pass

# Import the Flask application
from run import app

# Vercel entrypoint
handler = app
