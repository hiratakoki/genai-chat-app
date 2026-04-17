from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks):
    return model.encode(chunks)

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def search(query, chunks, chunk_vectors, top_k = 3):
    query_vec = embed_chunks([query])[0]
    scores =[]
    for chunk, vec in zip(chunks, chunk_vectors):
        sim = cosine_similarity(query_vec, vec)
        scores.append((sim, chunk))
    scores.sort(reverse = True)
    return [chunk for _, chunk in scores[:top_k]]

def chunk_text(text, chunk_size = 200, overlap = 50):
    start = 0
    finish = chunk_size
    textlist = []
    while(len(text) >= start):
        addtext = text[start: finish]
        textlist.append(addtext)
        addchunk = chunk_size - overlap
        start += addchunk
        finish += addchunk
    return textlist

if __name__ == "__main__":
    text = """
    Pythonはシンプルで読みやすいプログラミング言語です。
    機械学習やデータ分析に広く使われています。
    JavaScriptはWebブラウザで動くプログラミング言語です。
    フロントエンド開発に欠かせない技術です。
    RAGとは検索拡張生成の略で、外部知識をLLMに渡す技術です。
    """
    chunks = chunk_text(text, chunk_size=80, overlap=10)
    vectors = embed_chunks(chunks)
    results = search("機械学習について教えて", chunks, vectors, top_k=2)
    print("=== 検索結果 ===")
    for i, r in enumerate(results):
        print(f"{i+1}: {r}")