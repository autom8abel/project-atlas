from sqlalchemy import Column, Integer, String, Text
from app.db.base import Base

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False, unique=True)  # The user's likely question
    answer = Column(Text, nullable=False)                   # The assistant's response
    category = Column(String, default="general")            # e.g., "finance", "tax", "general"

    def __repr__(self):
        return f"<FAQ {self.id}: {self.question}>"
