
# Install — Windows 11 (PowerShell 7)

```powershell
mkdir C:\Agent, C:\Agent\{bin,config,models,logs,audit,ingest,src,tests,docs} -Force
py -3.11 -m venv C:\Agentenv
C:\Agentenv\Scripts\Activate.ps1
pip install -U pip wheel

pip install fastapi uvicorn pydantic requests mss pillow pytesseract sounddevice soundfile keyboard ^
  faster-whisper faiss-cpu sentence-transformers pypdf

choco install -y tesseract

winget install -e --id Ollama.Ollama
ollama pull qwen2.5:7b-instruct
# (Optional) ollama pull moondream:latest

# Piper: download CLI + en_US-amy-medium.onnx to C:\Agent\models\piper$env:PIPER_VOICE="C:\Agent\models\piper\en_US-amy-medium.onnx"

Copy-Item C:\Agent\config\config.example.json C:\Agent\config\config.json
$env:AGENT_CONFIG="C:\Agent\config\config.json"

pwsh -File C:\Agentingent.ps1 start
```
