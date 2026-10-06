"""rag.py - the brain of Telangana 360.

Flow:  data/*.txt  ->  chunks  ->  embeddings  ->  ChromaDB
       question    ->  embedding -> top matching chunks -> answer
"""
import re
from pathlib import Path

import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

BASE = Path(__file__).parent
DATA_DIR = BASE / "data"
DB_DIR = str(BASE / "chroma_db")

EMBED_MODEL = "all-MiniLM-L6-v2"      # turns text into meaning-numbers
GEN_MODEL = "google/flan-t5-base"     # writes the answer (use flan-t5-small if slow)
MAX_DISTANCE = 0.75                   # bigger = more lenient matching

_embedder = None
_tokenizer = None
_generator = None
_collection = None


def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL)
    return _embedder


def read_file(file):
    """Return the text of a .txt or .pdf file."""
    if file.suffix == ".pdf":
        reader = PdfReader(str(file))
        return "\n\n".join(page.extract_text() or "" for page in reader.pages)
    return file.read_text(encoding="utf-8")


def load_chunks():
    """Split every file in data/ into paragraphs (one paragraph = one chunk)."""
    ids, texts, metas = [], [], []
    files = sorted(list(DATA_DIR.glob("*.txt")) + list(DATA_DIR.glob("*.pdf")))
    for file in files:
        for i, para in enumerate(re.split(r"\n\s*\n", read_file(file))):
            para = para.strip()
            if len(para) > 40:
                ids.append(f"{file.stem}-{i}")
                texts.append(para)
                metas.append({"topic": file.stem})
    return ids, texts, metas


def get_collection(rebuild=False):
    """Open the vector database; build it from data/ if it is empty."""
    global _collection
    if _collection is not None and not rebuild:
        return _collection

    client = chromadb.PersistentClient(path=DB_DIR)
    if rebuild:
        try:
            client.delete_collection("telangana360")
        except Exception:
            pass
    col = client.get_or_create_collection(
        "telangana360", metadata={"hnsw:space": "cosine"}
    )
    if col.count() == 0:
        ids, texts, metas = load_chunks()
        embeddings = get_embedder().encode(texts).tolist()
        col.add(ids=ids, documents=texts, embeddings=embeddings, metadatas=metas)
    _collection = col
    return col


def retrieve(question, k=3):
    """Find the k chunks closest in meaning to the question."""
    col = get_collection()
    q_vec = get_embedder().encode([question]).tolist()
    res = col.query(query_embeddings=q_vec, n_results=k)
    results = []
    for text, meta, dist in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        if dist <= MAX_DISTANCE:
            results.append({"text": text, "topic": meta["topic"], "distance": dist})
    return results


def generate_answer(question, passages):
    """Let the language model write a short answer from the retrieved chunks."""
    global _tokenizer, _generator
    if _generator is None:
        _tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL)
        _generator = AutoModelForSeq2SeqLM.from_pretrained(GEN_MODEL)

    context = " ".join(p["text"] for p in passages)[:1500]
    prompt = (
        "Answer the question in 2-3 complete sentences using only the context.\n\n"
        f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
    )
    inputs = _tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    output = _generator.generate(**inputs, max_new_tokens=150, num_beams=4)
    return _tokenizer.decode(output[0], skip_special_tokens=True)