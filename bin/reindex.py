
import os, json, glob
from src.tools.rag import RAG, chunk_text
CFG = json.load(open(os.environ.get("AGENT_CONFIG", r"C:\Agent\config\config.example.json"), "r", encoding="utf-8"))
R = RAG(CFG["rag"]["index_dir"], CFG["rag"]["embed_model"])
def ingest_path(p):
    if p.lower().endswith(".pdf"):
        from pypdf import PdfReader
        txt=[]; r=PdfReader(p); [txt.append(pg.extract_text() or "") for pg in r.pages]; return "\n".join(txt)
    return open(p,"r",encoding="utf-8",errors="ignore").read()
def main():
    for root in (r"C:\Agent\ingest", *CFG["sandboxes"]):
        if not os.path.exists(root): continue
        for p in glob.glob(os.path.join(root,"**","*.*"), recursive=True):
            if not os.path.isfile(p): continue
            if not any(p.lower().endswith(ext) for ext in (".txt",".md",".pdf",".log",".py",".json",".cfg",".ini")): continue
            try:
                txt=ingest_path(p); R.add(p, chunk_text(txt, CFG["rag"]["chunk_size"], CFG["rag"]["chunk_overlap"])); print("Indexed:", p)
            except Exception as e:
                print("Err:", p, e)
if __name__=="__main__": main()
