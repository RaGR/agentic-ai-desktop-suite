
import os, time, glob
from pypdf import PdfReader
from src.tools.rag import RAG, chunk_text

WATCH_DIRS = [ r"C:\Agent\ingest" ]
INDEX_DIR = r"C:\Agent\models\rag"
EMB_MODEL = "BAAI/bge-small-en-v1.5"

def _read(path):
    if path.lower().endswith(".pdf"):
        txt=[]; r=PdfReader(path)
        for p in r.pages: txt.append(p.extract_text() or "")
        return "\n".join(txt)
    else:
        return open(path,"r",encoding="utf-8",errors="ignore").read()

def run():
    rag = RAG(INDEX_DIR, EMB_MODEL)
    seen = set()
    while True:
        for root in WATCH_DIRS:
            for p in glob.glob(os.path.join(root, "**","*.*"), recursive=True):
                if p in seen: continue
                if not os.path.isfile(p): continue
                if not any(p.lower().endswith(ext) for ext in (".txt",".md",".pdf",".log",".py",".json",".cfg",".ini")): continue
                try:
                    txt=_read(p); ch=chunk_text(txt,700,100)
                    rag.add(p, ch)
                    print("Indexed:", p); seen.add(p)
                except Exception as e:
                    print("Ingest error:", p, e)
        time.sleep(5)

if __name__=="__main__":
    run()
