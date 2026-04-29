from pydantic import BaseModel
from typing import Optional

class CoursCreate(BaseModel):
    nom: str
    description: Optional[str] = None

class CoursResponse(CoursCreate):
    id: int

    class Config:
        from_attributes = True