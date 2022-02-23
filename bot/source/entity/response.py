from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

@dataclass
class Response:
    message: str
    replyMarkup: Optional[object] = None
    photo: Optional[object] = None
