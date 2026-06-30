import os
import numpy as np
import voyageai
import json

VOYAGE_MODEL = "voyage-3.5"

class VectorStore:
    def __init__(self):
        self.client = voyageai.Client(api_key=os.environ["VOYAGE_API_KEY"])
        self.chunks = []
        self.embeddings = None

    def save(self, path: str):
        np.save(f"book_data/{path}_embeddings.npy", self.embeddings)
        with open(f"book_data/{path}_chunks.json", "w") as f:
            json.dump(self.chunks, f)

    def load(self, path: str):
        self.embeddings = np.load(f"book_data/{path}_embeddings.npy")
        with open(f"book_data/{path}_chunks.json", "r") as f:
            self.chunks = json.load(f)

    def build(self, chunks, batch_size=100):
        self.chunks = chunks
        texts = [c["text"] for c in chunks]

        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            result = self.client.embed(batch, model=VOYAGE_MODEL, input_type="document")
            all_embeddings.extend(result.embeddings)
        self.embeddings = np.array(all_embeddings)

    def search(self, query, top_k=5):
        if self.embeddings is None:
            raise ValueError("Vector Store has no embeddings, call build() first")

        try:
            res = self.client.embed([query], model=VOYAGE_MODEL, input_type="query")
            query_vec = np.array(res.embeddings[0])
            norms = np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_vec)
            sims = self.embeddings @ query_vec / norms
            top_indices = np.argsort(sims)[::-1][:top_k]

            return [
                {**self.chunks[i], "score": float(sims[i])}
                for i in top_indices
            ]
        except Exception as e:
            raise Error(e)