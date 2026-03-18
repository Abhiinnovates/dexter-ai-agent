from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


class VectorMemory:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)
        self.texts = []

    def add(self, text):

        vector = self.model.encode([text])
        self.index.add(np.array(vector).astype("float32"))

        self.texts.append(text)

    def search(self, query):

        vector = self.model.encode([query])
        D, I = self.index.search(np.array(vector).astype("float32"), 3)

        return [self.texts[i] for i in I[0]]


memory = VectorMemory()
