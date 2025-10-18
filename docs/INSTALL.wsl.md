
# Install — WSL2 Ubuntu 24.04 (optional RAG worker)
```bash
sudo apt update && sudo apt install -y python3-venv build-essential ffmpeg tesseract-ocr tesseract-ocr-eng tesseract-ocr-fas
python3 -m venv ~/agent/venv && source ~/agent/venv/bin/activate
pip install -U pip faiss-cpu sentence-transformers watchdog pypdf
# Copy code from Windows via \wsl$ and run an ingest worker if desired
```
