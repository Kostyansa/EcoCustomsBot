from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: int
    telegram_id: str
    role: str
    points: Optional[int]