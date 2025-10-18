
from src.tools.rag import RAG, chunk_text
import os, shutil, tempfile
def test_rag_query_roundtrip():
    d=tempfile.mkdtemp()
    R=RAG(d,"BAAI/bge-small-en-v1.5")
    R.add("x.txt", [(1,"hello world"), (10,"agent systems use tools")])
    out=R.query("tools")["hits"]
    shutil.rmtree(d)
    assert any("agent" in h["snippet"] for h in out)
