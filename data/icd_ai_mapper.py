from sentence_transformers import SentenceTransformer
import pandas as pd # to read file
from sklearn.metrics.pairwise import cosine_similarity # to compare vectors

# Load model ONCE
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load dataset
icd_data = pd.read_csv("icd10_codes.csv")

# Precompute embeddings
disease_embeddings = model.encode(icd_data["disease"].tolist())
#. converting the icd code to vectors

def map_icd_code_ai(text):

    if not text:
        return "Unknown"

    text = str(text)

    text_embedding = model.encode([text])
    # converting the input from prescription into vector

    similarities = cosine_similarity(text_embedding, disease_embeddings)
    # comparing the input vector with all vector list

    best_index = similarities.argmax()
    # finding best match

    return str(icd_data.iloc[best_index]["icd10_code"])
    # returnig the code