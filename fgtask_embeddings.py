# pip install sentence-transformers faiss-cpu pandas numpy
import pandas as pd
import numpy as np
import re
import faiss
from sentence_transformers import SentenceTransformer
import pickle

df = pd.read_csv('top_posts.csv')

def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # Remove URLs clearly
    text = re.sub(r"#", "", text)        # Remove '#' symbol but keep word clearly
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove special chars clearly
    text = re.sub(r"\s+", " ", text)     # Remove extra whitespace
    return text.strip()

df['text_cleaned'] = df['text'].apply(clean_text)

# df.head()

# Load embedding model (fast and effective)
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Generate embeddings for cleaned text of top posts
texts = df['text_cleaned'].tolist()
embeddings = embed_model.encode(texts, show_progress_bar=True)

# print(f"Embeddings shape: {embeddings.shape}")

# Define the dimension of embeddings
dimension = embeddings.shape[1]

# Initialize FAISS index (FlatL2 = simple & fast)
index = faiss.IndexFlatL2(dimension)

# Add embeddings to index
index.add(np.array(embeddings))

# print(f"Total embeddings in index: {index.ntotal}")

# Save FAISS index
faiss.write_index(index, 'linkedin_posts_index.faiss')

# Save texts
with open('linkedin_top_texts.pkl', 'wb') as f:
    pickle.dump(texts, f)

# Load saved FAISS index clearly
index = faiss.read_index('linkedin_posts_index.faiss')

# Load texts
with open('linkedin_top_texts.pkl', 'rb') as f:
    texts = pickle.load(f)

# Embedding model (must match the one from Step 1 exactly!)
embed_model = SentenceTransformer('all-MiniLM-L6-v2')


#Testing code

# def retrieve_similar_posts(query, k=3):
#     # Generate embedding for your input query/topic
#     query_embedding = embed_model.encode([query])

#     # Search FAISS index for similar posts
#     distances, indices = index.search(np.array(query_embedding), k)

#     # Retrieve actual texts
#     retrieved_posts = [texts[idx] for idx in indices[0]]

#     return retrieved_posts

# Example test retrieval
# test_topic = "AI applications in marketing products"
# retrieved_examples = retrieve_similar_posts(test_topic, k=3)

# print("Retrieved Posts (Clearly shown):\n")
# for idx, post in enumerate(retrieved_examples, start=1):
#     print(f"{idx}. {post}\n---\n")

