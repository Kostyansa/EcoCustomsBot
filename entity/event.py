from dataclasses import dataclass
from typing import Optional

@dataclass
class Event:
    id: int
    name: str
    code: str
    points: int
    date: str
    description: str