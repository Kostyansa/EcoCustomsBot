from dataclasses import dataclass
from typing import Optional
from enum import Enum

class Role(Enum):
    USER = 1
    ADMIN = 2
    
@dataclass
class User:
    id: int
    telegram_id: int
    points: Optional[int] = None
    role: Role = Role.USER
