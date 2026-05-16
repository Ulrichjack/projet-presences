from pydantic import BaseModel
from typing import Optional

class CoursCreate(BaseModel):
    nom: str
    description: Optional[str] = None
    code: str
    filiere: str
    niveau: str
    credits: int

class CoursResponse(CoursCreate):
    id: int

    class Config:
        from_attributes = True