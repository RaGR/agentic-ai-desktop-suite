# Local Agentic AI — Windows 11 + WSL2 (Phase-1 MVP)

Offline-first, local, multimodal **agent** with a **central LLM brain**. Push-to-talk voice → summarize a local file from sandbox with inline citations → speak the result. Includes read-only FS tools, allowlisted terminal, screen capture + OCR, minimal FAISS RAG, and JSON audit logs.

> **Assumptions**
> - OS: Windows 11, PowerShell 7; optional WSL2 Ubuntu 24.04 worker.
> - Python 3.11; NVIDIA GTX 960 (~4 GB VRAM) available but not required.
> - Offline after initial model/voice downloads.

---

## ✨ Features (Phase-1)

- **LLM runtime**: Ollama + `qwen2.5:7b-instruct` (quant **Q4_K_M**, ctx ≤ 8k).
- **Voice in/out**: faster-whisper (tiny/base int8), Piper TTS (local).  
- **Vision/OCR**: Screen capture (mss) → Tesseract (`eng+fas`).
- **RAG-lite**: FAISS + Sentence-Transformers (`bge-small-en-v1.5`), citations as `path#line`.
- **Tooling**: Read-only FS (`read_text|list_dir|stat`), allowlist shell (PowerShell + Bash).
- **Safety**: Sandboxed paths, allowlisted commands, hotkey-gated capture/PTT, comprehensive audit logs.
- **Observability**: Structured JSONL logs, per-tool audit entries with payload hash.

---

## 🧰 System Requirements

- CPU: Intel i7-6700HQ or better  
- GPU: GTX 960 (~4 GB VRAM) **recommended** for LLM offload (CPU fallback works)  
- RAM: 12 GB  
- Disk: 500 GB SSD  
- Software: Windows 11, PowerShell 7, Python 3.11, Chocolatey (for Tesseract), winget (for Ollama)

---

## 📦 Repository Layout

```

C:\Agent
bin\                 # operator scripts (start/stop/reindex, hotkeys)
config\              # config schema, example, allowlists
models\              # local models/voices/cache (you place voices here)
logs\                # runtime logs + generated audio/screens
audit\               # immutable per-tool audit logs (JSONL by date)
ingest\              # drop files here to index (in addition to sandboxes)
src\                 # Python services, tools, planner, runtime
tests\               # unit + smoke e2e aids
docs\                # install docs (Windows/WSL)
venv\                # created by setup script

```

---

## 🚀 Quickstart (10 Steps)

1. **Create folders**
   ```powershell
   mkdir C:\Agent, C:\Agent\{bin,config,models,logs,audit,ingest,src,tests,docs} -Force
    ```

2. **Create venv & install deps**

   ```powershell
   py -3.11 -m venv C:\Agent\venv
   C:\Agent\venv\Scripts\Activate.ps1
   pip install -U pip wheel
   pip install fastapi uvicorn pydantic requests mss pillow pytesseract sounddevice soundfile keyboard `
     faster-whisper faiss-cpu sentence-transformers pypdf
   ```
3. **OCR (Tesseract)**

   ```powershell
   choco install -y tesseract
   ```
4. **Ollama + model**

   ```powershell
   winget install -e --id Ollama.Ollama
   ollama pull qwen2.5:7b-instruct
   ```
5. **Piper voice**
   Download a Piper voice (e.g., `en_US-amy-medium.onnx`) into:

   ```
   C:\Agent\models\piper\
   ```

   Optionally set:

   ```powershell
   $env:PIPER_VOICE="C:\Agent\models\piper\en_US-amy-medium.onnx"
   ```
6. **Configs & allowlists**

   * Edit `config\config.example.json` with your sandbox paths.
   * Copy to `config.json` and export:

     ```powershell
     Copy-Item C:\Agent\config\config.example.json C:\Agent\config\config.json
     $env:AGENT_CONFIG="C:\Agent\config\config.json"
     ```
7. **Index some content**

   * Put files in `C:\Agent\ingest` and/or your sandboxes.
   * Build the index:

     ```powershell
     python C:\Agent\bin\reindex.py
     ```
8. **Start services**

   ```powershell
   pwsh -File C:\Agent\bin\agent.ps1 start
   ```
9. **Use hotkeys**

   * **PTT** `Ctrl+Space`: speak a request.
   * **Screen** `Ctrl+Alt+S`: capture → OCR dump to console.
10. **Demo the MVP**
    Say:

    > “Summarize the key tasks from ‘C:\Users<YOU>\Projects\todo.md’ and cite the file.”

    Expect spoken bullets + audit entries in `C:\Agent\audit\YYYY-MM-DD.jsonl`.

---

## ⚙️ Configuration

* **Schema**: `config/config.schema.json`
* **Example**: `config/config.example.json`

Key fields:

* `runtime.engine`: `"ollama"`
* `runtime.model`: `"qwen2.5:7b-instruct"`
* `runtime.quant`: `"q4_K_M"`
* `runtime.context_tokens`: `8192`
* `languages`: `{ stt: "en", tts: "en", ocr: "eng+fas" }`
* `safety`: `{ terminal_mode: "allowlist", require_confirm_destructive: true, screen_capture_hotkey, ptt_hotkey }`
* `sandboxes`: array of absolute paths (read-only in Phase-1)
* `rag`: `{ embed_model, chunk_size, chunk_overlap, top_k, index_dir }`

---

## ⌨️ Hotkeys

* **Push-to-talk**: `Ctrl+Space`
* **Screen capture**: `Ctrl+Alt+S` (full screen → `logs\screen.png` → OCR)

Change hotkeys in `config.json` and restart the agent.

---

## 🔌 API (Local)

Base: `http://127.0.0.1:8088`

* `POST /chat` — `{ "text": "..." }` → planner routes tools, returns `{ ok, text }`.
* `POST /tools/fs` — `{ op, path }` where `op ∈ {read_text,list_dir,stat}`.
* `POST /tools/shell` — `{ shell, cmd, cwd? }` with allowlist enforcement.
* `POST /tools/rag/query` — `{ q, top_k? }` → FAISS hits with `path#line`.
* `POST /tools/screen/capture` — `{ mode, region? }` → `{ image_path }`.
* `POST /tools/ocr` — `{ image_path, lang?, psm? }` → `{ text }`.
* `POST /tools/stt` — `{ audio_path?, size?, language? }` → `{ text }`.
* `POST /tools/tts` — `{ text }` → writes `logs\out.wav` (or SAPI speaks if no Piper).

Every endpoint creates an **audit record**: `C:\Agent\audit\YYYY-MM-DD.jsonl`.

---

## 🔐 Security & Safety (Phase-1)

* **Filesystem**: Read-only tools inside configured **sandboxes**. Path normalization; traversal denied.
* **Terminal**: **Allowlist-only** commands. No destructive ops.
* **Capture & Voice**: Both gated by **hotkeys** (PTT, Screen).
* **Network**: Localhost APIs only. No external calls after model/voice pulls.
* **Audit**: Per-tool JSONL with payload hash, result, timestamps.

---

## 🧱 RAG Ingest

* Watch / index locations: `C:\Agent\ingest` and configured sandboxes.
* Supported: `.txt .md .pdf .log .py .json .cfg .ini` (extend in scripts).
* Chunking: default `700/100`.
* Embeddings: `bge-small-en-v1.5` (CPU).
* Store: FAISS index + `metadata.sqlite` (in `models\rag`).

Rebuild on demand:

```powershell
python C:\Agent\bin\reindex.py
```

---

## 🧪 Testing

* **Unit**: safety checks, allowlist parsers, RAG round-trip, OCR smoke.
* **E2E (manual)**: Start agent → `Ctrl+Space` → speak the summarize request → expect TTS + citations + audit entries.

Run unit tests (example):

```powershell
C:\Agent\venv\Scripts\Activate.ps1
pytest -q
```

---

## 🛠️ Troubleshooting

* **LLM slow / OOM**: Reduce context to 4k; keep `q4_K_M`; let Ollama offload fewer layers; CPU fallback acceptable.
* **No audio device**: Check `sounddevice` default input/output; set system default; try 16 kHz mono via `bin\hotkeys.py`.
* **OCR poor**: Increase contrast; use region capture; try `psm=6`. Ensure Tesseract language packs installed.
* **Allowlist denies**: Edit `config\terminal.allowlist.*.txt`; restart agent.
* **Sandbox denied**: Verify absolute path is under one of `sandboxes` and no traversal.

Logs: `C:\Agent\logs\agent.jsonl`
Audits: `C:\Agent\audit\YYYY-MM-DD.jsonl`

---

## 📈 Performance Notes

* Target TTF (first token) < 3 s with 7B Q4 on GTX-960 partial offload.
* STT `base` int8 is near real-time on CPU; use `tiny` for very low latency.
* Piper TTS is real-time-ish on CPU for short sentences.
* Keep RAG `top_k` small (≤6) and chunks ~700 for speed.

---

## 🚫 Known Limitations (Phase-1)

* No FS write/move/delete; read-only operations only.
* No destructive shell commands; **advanced mode** disabled.
* Vision-chat (e.g., LLaVA, Moondream) not required for DoD.
* English-first embeddings; multilingual retrieval is limited.

---

## 🗺️ Roadmap → Phase-2/3 (High-Level)

* **Phase-2**: Write ops with typed confirmation, hybrid retrieval (BM25+dense) + reranker, richer planner (LangGraph), metrics/OTel, WSL worker service.
* **Phase-3**: Chaos/security tests, backups/restore, wake word, advanced terminal mode with PIN, air-gapped packaging.

---

## 📜 License

Apache-2.0

---

## 👤 Credits

Built for a Windows 11 + WSL2 local-first environment with strict safety defaults and audited tooling.

