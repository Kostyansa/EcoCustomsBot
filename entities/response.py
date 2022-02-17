from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

@dataclass
class Response:
    rowid: int
    name: str
    message: str

class Action(Enum):
    NOTHING = 1