from sentence_transformers import SentenceTransformer, util
import re

model = SentenceTransformer("all-MiniLM-L6-v2")

def similarity_score(answer: str, context: str) -> float:

    def clean_text(t: str) -> str:
        return re.sub(r'[^a-z0-9\s]', '', t.lower().strip())

    clean_answer = clean_text(answer)
    clean_context = clean_text(context)
    if not clean_answer or not clean_context:
        return 0.0
    emb1 = model.encode(clean_answer, convert_to_tensor=True)
    emb2 = model.encode(clean_context, convert_to_tensor=True)
    raw_sim = util.cos_sim(emb1, emb2).item()

    # Normalize cosine similarity from [-1,1] → [0,1]
    normalized = (raw_sim + 1) / 2
    human_scaled = normalized ** 0.7

    return round(human_scaled, 3)
