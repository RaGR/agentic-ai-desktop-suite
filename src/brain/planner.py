
import os, re
from src.tools import fs as tfs, rag as trag, tts as ttts
from src.brain.runtime import Ollama
from src.common.logging import audit

SUMMARIZE_PAT = re.compile(r"(summari[sz]e).*(file|document)", re.I)

def summarize_file(flow, path:str, sandboxes, rag:trag.RAG, llm:Ollama, voice_model=None):
    r = tfs.read_text(path, sandboxes)
    if not r.get("ok"): return {"ok":False,"error":"fs_read_failed", "detail":r}
    text = r["text"]
    chunks = trag.chunk_text(text, size=1200, overlap=100)
    sys_prompt = "You are a precise assistant. Summarize key tasks and conclusions. Include inline citations as (path:line). Keep it crisp."
    user_prompt = f"File: {path}\nProvide a brief bullet summary with citations using the line numbers shown below.\n"
    sample = []
    for (ln,chunk) in chunks[:3]:
        sample.append(f"[start_line={ln}]\n{chunk[:1800]}")
    user_prompt += "\n\n".join(sample)
    content = llm.chat([{"role":"system","content":sys_prompt},{"role":"user","content":user_prompt}])
    ttts.speak(content, voice_model_path=voice_model)
    audit("planner.summarize_file", {"path":path}, {"ok":True,"chars":len(content)})
    return {"ok":True,"text":content}

def plan(flow, text:str, sandboxes, rag:trag.RAG, llm:Ollama, voice_model=None):
    m = SUMMARIZE_PAT.search(text or "")
    if m:
        path = None
        q = re.search(r"[\"']([^\"']+\.(md|txt|log|py|pdf))[\"']", text, re.I)
        if q: path = q.group(1)
        if not path:
            p = re.search(r"in\s+([A-Za-z]:\\[^\\\n]+(?:\.[A-Za-z0-9]+)?)", text)
            if p: path=p.group(1)
        if not path:
            return {"ok":False,"error":"no_path_found","hint":"Specify full path or quoted filename."}
        return summarize_file(flow, path, sandboxes, rag, llm, voice_model)
    out = llm.chat([{"role":"system","content":"You are concise."},{"role":"user","content":text}])
    return {"ok":True,"text":out}
