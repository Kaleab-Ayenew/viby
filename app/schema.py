from pydantic import BaseModel
from typing import Optional

class Command(BaseModel):
    command: str
    comment: Optional[str] = None

