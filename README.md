# 🧠 Local Agentic AI OS — The Offline AI Brain for Your Machine

A **local-first, multimodal, agentic AI operating layer** for **Windows 11 + WSL2**.  
It turns your personal computer into an **autonomous, privacy-preserving assistant** that can *see, hear, read, reason, and act* on your system — **without any cloud dependency**.

---

## 🌌 The Vision

> “Your computer should be intelligent — not dependent.”

This project is built around a simple idea:  
**What if your computer could reason and operate like a personal AI OS — all offline?**

Modern AI assistants rely on cloud APIs that stream your data to third-party servers.  
**Local Agentic AI OS** breaks that model — hosting the entire intelligence stack locally, giving you:

- 🔒 **Privacy** — nothing leaves your system.  
- ⚡ **Performance** — no latency, full GPU acceleration.  
- 🧩 **Extensibility** — plug in tools, agents, and workflows like system modules.  
- 🧠 **Continuity** — one persistent “brain” coordinating your data, files, and commands.

Think of it as your **local GPT-based kernel**:  
a unified AI layer that orchestrates speech, vision, file operations, and reasoning across your OS.

---

## 🧩 Core Concept

The system is designed around a **central LLM brain** (the planner), which interprets natural language commands and delegates them to **safe, audited tools**.  
Every interaction passes through **policy gates**, ensuring full control and traceability.

### 🧠 Central Brain
- **Model:** `qwen2.5:7b-instruct` (via **Ollama**)
- **Context window:** 8 K tokens (configurable)
- **Quantization:** Q4_K_M for GTX 960-class GPUs
- **Role:** Plan tasks, parse intents, invoke tools (FS, RAG, OCR, etc.)

### ⚙️ Tooling Layer
- **Filesystem:** read-only exploration and summarization
- **Terminal:** allowlisted PS/Bash commands
- **RAG:** FAISS + BGE embeddings for local document retrieval
- **Vision:** screen capture + Tesseract OCR
- **Audio:** faster-whisper STT + Piper TTS

### 🔒 Safety Layer
- Path-scoped sandboxes  
- Command allowlists  
- Explicit hotkeys (no background listening)  
- JSON audit logs for every action  

---

## 🧬 Architecture Overview

```

+--------------------+       +---------------------------+
|   User Interface   | <---->|   Hotkeys / Tray / CLI    |
| (PTT, Capture, UI) |       |  (Ctrl+Space / Ctrl+Alt+S)|
+---------+----------+       +-------------+-------------+
|
v
+----------------------+      +-----------------------------+
|     Orchestrator     | <--> |   Policy & Safety Engine    |
|  (Planner, Tool Calls)|     |  (Allowlist, Sandboxes)     |
+----------+-----------+      +--------------+--------------+
|                                          |
v                                          v
+----------+-----------+              +---------------+--------------+
|        Tools         |              |         Logging/Audit        |
| FS | RAG | Shell | STT|             | JSONL logs, per-tool audits  |
| TTS| OCR | Screen    |              | (immutability, payload hash) |
+----------+-----------+              +---------------+--------------+
|
v
+----------+-------------------------------------------+
|       LLM Brain  (Ollama + Qwen 7B Q4)              |
|  Chat planner / summarizer / reasoning engine        |
+------------------------------------------------------+

````

---

## ⚙️ Features

| Domain | Capability | Local Backend |
|---------|-------------|---------------|
| **Language** | LLM planner (reasoning, summarizing, coding) | Ollama + Qwen2.5 |
| **Speech In** | Push-to-talk transcription | faster-whisper (base int8) |
| **Speech Out** | Offline voice generation | Piper TTS (ONNX) |
| **Vision** | Screen capture + OCR | MSS + Tesseract (eng+fas) |
| **Knowledge** | Vector search + citations | FAISS + BGE-small |
| **System** | File read, safe shell, logs | PowerShell 7 / WSL bash |
| **Security** | Sandboxes, allowlists, audits | Built-in policies |
| **Observability** | Structured JSONL logs | `logs/` + `audit/` |
| **Offline Mode** | Fully functional after downloads | ✅ |

---

## 🚀 Quickstart (Windows 11)

1. **Clone or copy project**

   ```powershell
   git clone https://github.com/yourname/local-agentic-ai-os-core.git C:\Agent
   cd C:\Agent
``

2. **Setup Python**

   ```powershell
   py -3.11 -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -U pip wheel
   pip install fastapi uvicorn pydantic requests mss pillow pytesseract sounddevice soundfile keyboard `
     faster-whisper faiss-cpu sentence-transformers pypdf
   ```

3. **Install OCR / LLM / TTS runtimes**

   ```powershell
   choco install -y tesseract
   winget install -e Ollama.Ollama
   ollama pull qwen2.5:7b-instruct
   ```

   Download Piper voice (e.g. `en_US-amy-medium.onnx`) to `C:\Agent\models\piper\`.

4. **Configure**

   Edit `config\config.example.json` → set your `sandboxes` (e.g. `C:\Users\<YOU>\Projects`).
   Copy it as `config.json`.

5. **Re-index knowledge**

   ```powershell
   python bin\reindex.py
   ```

6. **Start agent**

   ```powershell
   pwsh -File bin\agent.ps1 start
   ```

7. **Use hotkeys**

   * `Ctrl + Space` → speak a command
   * `Ctrl + Alt + S` → screen capture → OCR

   Example:

   > “Summarize the key tasks from `C:\Users\<YOU>\Projects\todo.md` and cite the file.”

---

## 🔊 Typical Flow

1. **Voice Input** → recorded by push-to-talk.
2. **STT** → transcribed text passed to planner.
3. **Planner** → routes intent (“summarize file”) → tool calls.
4. **Tools** → FS read + RAG query + LLM summary.
5. **Response** → TTS speaks result.
6. **Audit** → all actions logged with hashes for traceability.

---

## 🧱 Design Philosophy

| Principle               | Meaning                                                              |
| ----------------------- | -------------------------------------------------------------------- |
| **Local-first**         | Every model and process runs on your hardware.                       |
| **Agentic**             | The AI can plan and use tools autonomously within safe boundaries.   |
| **Modular**             | Each capability (STT, OCR, RAG, etc.) is a detachable micro-service. |
| **Auditable**           | Nothing happens silently — every action is logged.                   |
| **Security-by-default** | No write ops, destructive commands, or hidden network access.        |
| **Human-in-loop**       | Push-to-talk and confirmations keep control in the operator’s hands. |

---

## 🛡️ Security Architecture

* **Sandboxes** — explicitly scoped folders; no access outside.
* **Terminal allowlists** — only safe commands (e.g. `dir`, `ls`, `git status`).
* **Policy engine** — denies traversal (`..`), shells with special chars, or advanced mode unless toggled.
* **Audit system** — per-tool logs with SHA-hashed payloads.
* **Air-gapped readiness** — network access not required after model pulls.

---

## 🧠 Example Use-Cases

| Category             | Example                                                            |
| -------------------- | ------------------------------------------------------------------ |
| **Productivity**     | “Summarize today’s meeting notes in Projects folder.”              |
| **Code assistance**  | “List Python files larger than 5 KB in my project directory.”      |
| **System awareness** | “Show me what’s inside the logs folder.”                           |
| **Research**         | “Search my documentation for ‘FAISS’ and quote the relevant line.” |
| **Accessibility**    | Speak documents aloud, read on-screen text.                        |

---

## 🧩 Configuration Overview

* `runtime` — LLM engine + parameters.
* `languages` — STT/TTS/OCR language codes.
* `safety` — terminal mode, confirmation, hotkeys.
* `sandboxes` — array of permitted directories.
* `rag` — embedding model, chunk sizes, overlap, index path.
* `logging` — verbosity level.

---

## 🧪 Testing & Evaluation

Run:

```powershell
pytest -q
```

**Metrics**

| Component    | Target                   |
| ------------ | ------------------------ |
| LLM latency  | < 3 s TTF                |
| STT accuracy | < 12 % WER (base int8)   |
| TTS latency  | < 1.5 s per sentence     |
| OCR accuracy | > 90 % UI text           |
| RAG hit-rate | > 70 % Top-1 correct doc |

---

## ⚙️ Troubleshooting

| Issue         | Solution                                       |
| ------------- | ---------------------------------------------- |
| GPU OOM       | reduce context to 4 k; lower offload layers    |
| No audio      | check input/output devices; ensure 16 kHz mono |
| OCR garbled   | install Tesseract `eng` and `fas`; use `psm=6` |
| Policy denial | verify allowlist + sandbox paths               |
| Index stale   | re-run `python bin\reindex.py`                 |

Logs → `C:\Agent\logs\agent.jsonl`
Audits → `C:\Agent\audit\YYYY-MM-DD.jsonl`

---

## 📜 License

Licensed under the **Apache License 2.0**
See the [`LICENSE`](./LICENSE) file for details.

---

## 🌍 Roadmap

| Phase                | Focus                                                     | Outcome                   |
| -------------------- | --------------------------------------------------------- | ------------------------- |
| **1. MVP (Current)** | Voice → File Summary → Speech Out                         | Fully offline core        |
| **2. Beta**          | Write ops, confirmations, hybrid RAG, reranker, better UI | Interactive desktop agent |
| **3. Prod**          | Wake-word, security suite, air-gapped bundle              | Private AI OS             |

---

## 🤝 Contributing

Pull requests and feature ideas welcome!
Focus on:

* Additional tool adapters (web, file ops, Git, API)
* Vision expansion (LLaVA/Moondream)
* Performance optimizations and UI front ends.

---

## 🧠 Summary

> **Local Agentic AI OS** is not just another chatbot —
> it’s an **operating layer of intelligence** that lives entirely on your machine.
> Voice, vision, reasoning, and command — unified in one offline, audited, private system.

Turn your PC into your **own autonomous AI operator**.
