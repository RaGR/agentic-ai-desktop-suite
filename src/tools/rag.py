
import os, sqlite3, faiss, numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
from src.common.logging import audit

class RAG:
    def __init__(self, index_dir:str, embed_model:str):
        self.index_dir = index_dir; os.makedirs(index_dir, exist_ok=True)
        self.db = os.path.join(index_dir, "metadata.sqlite")
        self.idx_path = os.path.join(index_dir, "faiss.index")
        self.model = SentenceTransformer(embed_model, device="cpu")
        self.dim = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.dim)
        if os.path.exists(self.idx_path):
            self.index = faiss.read_index(self.idx_path)
        self._conn = sqlite3.connect(self.db)
        self._conn.execute("""CREATE TABLE IF NOT EXISTS chunks(
            id INTEGER PRIMARY KEY, path TEXT, start_line INTEGER, text TEXT)""")
        self._conn.commit()

    def _embed(self, texts:List[str]):
        em = self.model.encode(texts, batch_size=32, normalize_embeddings=True)
        return em.astype("float32")

    def add(self, path:str, chunks:List[Tuple[int,str]]):
        if not chunks: return
        vecs = self._embed([c[1] for c in chunks])
        start_id = self.index.ntotal
        self.index.add(vecs)
        with self._conn:
            for i,(ln,txt) in enumerate(chunks):
                self._conn.execute("INSERT INTO chunks(id,path,start_line,text) VALUES(?,?,?,?)",
                                   (start_id+i, path, ln, txt))
        faiss.write_index(self.index, self.idx_path)

    def query(self, q:str, top_k:int=6):
        if self.index.ntotal==0: return {"ok":True,"hits":[]}
        qv = self._embed([q])
        D,I = self.index.search(qv, top_k)
        cur = self._conn.cursor()
        hits=[]
        for idx,score in zip(I[0], D[0]):
            cur.execute("SELECT path,start_line,text FROM chunks WHERE id=?", (int(idx),))
            row=cur.fetchone()
            if row: hits.append({"path":row[0], "line":row[1], "snippet":row[2][:400], "score":float(score)})
        audit("rag.query", {"q":q,"top_k":top_k}, {"ok":True,"hits":len(hits)}); return {"ok":True,"hits":hits}

def chunk_text(txt:str, size:int=700, overlap:int=100):
    lines=txt.splitlines(); chunks=[]; cur=[]; cur_len=0; start_line=1
    for i,l in enumerate(lines, start=1):
        if cur_len+len(l) > size and cur:
            chunks.append((start_line, "\n".join(cur)))
            cur=[l]; cur_len=len(l); start_line=i
        else:
            cur.append(l); cur_len+=len(l)
    if cur: chunks.append((start_line, "\n".join(cur)))
    return chunks
