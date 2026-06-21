from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

model = SentenceTransformer('all-MiniLM-L6-v2')

sentence1 = "I want to become an AI engineer"
sentence2 = "My goal is to work in artificial intelligence"
sentence3 = "I bought groceries today"

embedding1 = model.encode(sentence1)
embedding2 = model.encode(sentence2)
embedding3 = model.encode(sentence3)

print("Similar meaning:", cos_sim(embedding1, embedding2))
print("Different meaning:", cos_sim(embedding1, embedding3))