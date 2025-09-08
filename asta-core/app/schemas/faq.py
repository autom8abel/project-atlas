from pydantic import BaseModel

class FAQBase(BaseModel):
    question: str
    answer: str
    category: str = "general"

class FAQCreate(FAQBase):
    pass

class FAQ(FAQBase):
    id: int

    class Config:
        from_attributes = True  # Allows ORM mode (formerly 'orm_mode')
