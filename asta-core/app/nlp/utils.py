import spacy
from typing import List
from app.models.faq import FAQ

# Load the medium English model.
nlp = spacy.load("en_core_web_md")

def find_most_similar_faq(user_question: str, faqs: List[FAQ]) -> FAQ | None:
    """
    Compares a user's question to a list of FAQs and returns the most similar one.
    Uses spaCy's word vector similarity.
    """
    if not faqs:
        return None

    user_doc = nlp(user_question.lower().strip())

    best_faq = None
    highest_similarity = -1.0

    for faq in faqs:
        faq_doc = nlp(faq.question.lower().strip())
        similarity = user_doc.similarity(faq_doc)
        print(f"DEBUG: '{user_question}' vs '{faq.question}' = {similarity}")
        
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_faq = faq

    if highest_similarity < 0.6:
        return None

    return best_faq
