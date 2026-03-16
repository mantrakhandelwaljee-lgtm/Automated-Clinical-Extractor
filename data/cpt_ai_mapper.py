import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

cpt_data = pd.read_csv("cpt_codes.csv")

procedure_embeddings = model.encode(cpt_data["procedure"].tolist())

def map_cpt_code_ai(text):

    if not text:        # handle None or empty text
        return "Unknown"

    text = str(text)

    text_embedding = model.encode([text])

    similarities = cosine_similarity(text_embedding, procedure_embeddings)

    best_index = similarities.argmax()

    return str(cpt_data.iloc[best_index]["cpt_code"])

# similar as icd_ai_mapper