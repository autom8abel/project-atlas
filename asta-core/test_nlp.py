# test_nlp.py
import sys
sys.path.append('/app')

from app.nlp.utils import find_most_similar_faq

# Mock FAQ objects (like what would come from the database)
class MockFAQ:
    def __init__(self, id, question, answer):
        self.id = id
        self.question = question
        self.answer = answer

mock_faqs = [
    MockFAQ(1, "What business expenses are tax deductible?", "Test answer 1"),
    MockFAQ(2, "How should I format my invoices?", "Test answer 2")
]

# Test the function
test_question = "what can i deduct?"
result = find_most_similar_faq(test_question, mock_faqs)

if result:
    print(f"SUCCESS! Question: '{test_question}' matched to: '{result.question}'")
else:
    print("No match found.")
