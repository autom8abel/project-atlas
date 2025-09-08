from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from app.db.session import get_db
from app.schemas.faq import FAQ, FAQCreate
from app.models.faq import FAQ as FAQModel
from app.nlp.utils import find_most_similar_faq

class QuestionRequest(BaseModel):
    question: str

router = APIRouter()

@router.post("/ask", response_model=FAQ)
async def ask_question(request: QuestionRequest, db: AsyncSession = Depends(get_db)):
    """
    Ask ASTA a question. It will find the most relevant FAQ answer.
    """
    # 1. Get all FAQs from the database
    result = await db.execute(select(FAQModel))
    all_faqs = result.scalars().all()

    # 2. Use NLP to find the best match
    best_faq = find_most_similar_faq(request.question, all_faqs)

    if not best_faq:
        raise HTTPException(
            status_code=404,
            detail="I couldn't find a good answer for that question. Please try rephrasing."
        )

    return best_faq

@router.post("/", response_model=FAQ, status_code=201)
async def create_faq(faq_data: FAQCreate, db: AsyncSession = Depends(get_db)):
    """Create a new FAQ entry (for admin use)."""
    new_faq = FAQModel(**faq_data.dict())
    db.add(new_faq)
    await db.commit()
    await db.refresh(new_faq)
    return new_faq
