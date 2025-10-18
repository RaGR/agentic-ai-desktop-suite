
import requests
from src.common.logging import log

class Ollama:
    def __init__(self, base="http://127.0.0.1:11434", model="qwen2.5:7b-instruct", ctx=8192):
        self.base=base.rstrip("/"); self.model=model; self.ctx=ctx
    def chat(self, messages, temperature=0.3):
        url=f"{self.base}/api/chat"
        payload={"model":self.model,"messages":messages,"options":{"temperature":temperature,"num_ctx":self.ctx}}
        r=requests.post(url,json=payload,timeout=120)
        r.raise_for_status(); data=r.json()
        log({"event":"ollama.chat","tokens":data.get("eval_count",0)})
        return data["message"]["content"]
