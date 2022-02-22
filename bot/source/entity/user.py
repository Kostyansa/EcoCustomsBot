from dataclasses import dataclass
from typing import Optional
from enum import Enum

class Role(Enum):
    USER = 0
    ADMIN = 1
    
@dataclass
class User:
    id: int
    telegram_id: str
    points: Optional[int]
    role: Role = Role.USER
