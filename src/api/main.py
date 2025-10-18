
import os, json
from fastapi import FastAPI, Body
from pydantic import BaseModel
from src.common.logging import log
from src.tools import fs, shell, screen, ocr, stt, tts, rag
from src.brain.runtime import Ollama
from src.brain import planner

CFG_PATH = os.environ.get("AGENT_CONFIG", r"C:\Agent\config\config.example.json")
CFG = json.load(open(CFG_PATH, "r", encoding="utf-8"))

app = FastAPI(title="Agent API", version="0.1")

SAND = CFG["sandboxes"]
PS_ALLOW = [l.strip() for l in open(r"C:\Agent\config\terminal.allowlist.ps1.txt","r",encoding="utf-8")]
BASH_ALLOW = [l.strip() for l in open(r"C:\Agent\config\terminal.allowlist.bash.txt","r",encoding="utf-8")]
RAG = rag.RAG(CFG["rag"]["index_dir"], CFG["rag"]["embed_model"])
LLM = Ollama(base=CFG["runtime"]["ollama_url"], model=CFG["runtime"]["model"], ctx=CFG["runtime"]["context_tokens"])
VOICE_MODEL = os.environ.get("PIPER_VOICE", r"C:\Agent\models\piper\en_US-amy-medium.onnx")

@app.post("/tools/fs")
def fs_endpoint(op:str=Body(...), path:str=Body(...)):
    if op=="read_text": return fs.read_text(path, SAND)
    if op=="list_dir":  return fs.list_dir(path, SAND)
    if op=="stat":      return fs.stat(path, SAND)
    return {"ok":False,"error":"unsupported_op"}

class ShellReq(BaseModel):
    shell:str; cmd:str; cwd:str|None=None

@app.post("/tools/shell")
def shell_endpoint(req: ShellReq):
    mode = CFG["safety"]["terminal_mode"]
    return shell.run(req.shell, req.cmd, req.cwd, mode, PS_ALLOW, BASH_ALLOW)

@app.post("/tools/screen/capture")
def screen_capture(mode:str="full", region:list[int]|None=None):
    return screen.capture(mode=mode, region=region)

@app.post("/tools/ocr")
def ocr_endpoint(image_path:str=Body(...), lang:str=Body(default=CFG["languages"]["ocr"]), psm:int=Body(default=3)):
    return ocr.ocr_image(image_path, lang, psm)

@app.post("/tools/stt")
def stt_endpoint(size:str="base", language:str=CFG["languages"]["stt"], audio_path:str|None=None):
    return stt.transcribe(audio_path=audio_path, size=size, language=language)

@app.post("/tools/tts")
def tts_endpoint(text:str=Body(...)):
    return tts.speak(text, voice_model_path=VOICE_MODEL)

@app.post("/tools/rag/query")
def rag_query(q:str=Body(...), top_k:int=Body(default=CFG["rag"]["top_k"])):
    return RAG.query(q, top_k)

@app.post("/chat")
def chat(text:str=Body(...)):
    res = planner.plan("flow0", text, SAND, RAG, LLM, voice_model=VOICE_MODEL)
    log({"event":"chat","ok":res.get("ok"),"len":len(res.get("text",""))})
    return res
