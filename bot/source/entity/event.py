from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Event:
    id: int
    name: str
    code: str
    points: int
    date: datetime
    description: str