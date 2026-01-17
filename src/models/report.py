from dataclasses import dataclass
from typing import Optional


@dataclass
class Report:
    user_id: int
    latitude: float
    longitude: float
    category: str
    subcategory: str
    description: str
    photo_file_id: Optional[str] = None
    audio_file_id: Optional[str] = None
