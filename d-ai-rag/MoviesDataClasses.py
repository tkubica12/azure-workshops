from pydantic import BaseModel, ValidationError
from typing import List

class EnhancedMovie(BaseModel):
    genres: List[str]
    characters: List[str]
    themes: List[str]
    setting: List[str]
    series: List[str]