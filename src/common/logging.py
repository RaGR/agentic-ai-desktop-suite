
import json, os, datetime, hashlib
LOG_DIR = os.environ.get("AGENT_LOG_DIR", r"C:\Agent\logs")
AUDIT_DIR = os.environ.get("AGENT_AUDIT_DIR", r"C:\Agent\audit")
os.makedirs(LOG_DIR, exist_ok=True); os.makedirs(AUDIT_DIR, exist_ok=True)

def _ts(): return datetime.datetime.utcnow().isoformat()+"Z"

def log(event: dict, fname="agent.jsonl"):
    event = {"ts": _ts(), **event}
    with open(os.path.join(LOG_DIR, fname), "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False)+"\n")

def audit(tool:str, payload:dict, result:dict):
    day = datetime.date.today().isoformat()
    s = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()
    aid = f"{tool}_{_ts()}_{hashlib.sha256(s).hexdigest()[:12]}"
    entry = {"ts": _ts(), "audit_id": aid, "tool": tool, "payload": payload, "result": result}
    with open(os.path.join(AUDIT_DIR, f"{day}.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False)+"\n")
    return aid
