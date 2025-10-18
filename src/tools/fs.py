
import os, hashlib
from src.policy.safety import normalize_path, is_in_sandboxes, deny_traversal
from src.common.logging import audit

def read_text(path: str, sandboxes):
    if deny_traversal(path) or not is_in_sandboxes(path, sandboxes):
        res={"ok":False,"error":"path_not_allowed","path":path}
        audit("fs.read_text", {"path":path}, res); return res
    p = normalize_path(path)
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        txt = f.read()
    res = {"ok":True,"bytes":len(txt.encode("utf-8")),"sha256":hashlib.sha256(txt.encode()).hexdigest()[:16],"text":txt}
    audit("fs.read_text", {"path":p}, {"ok":True,"bytes":res["bytes"]}); return res

def list_dir(path: str, sandboxes):
    if deny_traversal(path) or not is_in_sandboxes(path, sandboxes):
        res={"ok":False,"error":"path_not_allowed","path":path}
        audit("fs.list_dir", {"path":path}, res); return res
    p = normalize_path(path)
    items = []
    for name in os.listdir(p):
        fp = os.path.join(p, name)
        try:
            items.append({"name":name,"is_dir":os.path.isdir(fp),"size":os.path.getsize(fp)})
        except FileNotFoundError:
            continue
    res={"ok":True,"items":items}
    audit("fs.list_dir", {"path":p}, {"ok":True,"count":len(items)}); return res

def stat(path: str, sandboxes):
    if deny_traversal(path) or not is_in_sandboxes(path, sandboxes):
        res={"ok":False,"error":"path_not_allowed","path":path}
        audit("fs.stat", {"path":path}, res); return res
    p = normalize_path(path)
    st = os.stat(p)
    res={"ok":True,"size":st.st_size,"mtime":st.st_mtime,"path":p}
    audit("fs.stat", {"path":p}, res); return res
